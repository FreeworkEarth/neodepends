//! Override detection for Python and Java.
//!
//! Detects when child classes override methods from parent classes:
//! - Python: Methods that override @abstractmethod decorated methods
//! - Java: Methods with @Override annotation

use std::collections::HashMap;
use std::collections::HashSet;

use tree_sitter::Parser;
use tree_sitter::Query;
use tree_sitter::QueryCursor;

use crate::core::ContentId;
use crate::core::Dep;
use crate::core::DepKind;
use crate::core::Entity;
use crate::core::EntityDep;
use crate::core::EntityId;
use crate::core::EntityKind;
use crate::core::PartialPosition;
use crate::core::PseudoCommitId;
use crate::filesystem::FileReader;
use crate::languages::Lang;

/// Detect override dependencies from entities and existing dependencies.
///
/// Takes entities, existing deps (to find Extend relationships), and a file reader.
/// Returns additional Override dependencies.
pub fn detect_overrides<R: FileReader>(
    entities: &[Entity],
    deps: &[EntityDep],
    reader: &R,
) -> Vec<EntityDep> {
    // Build indices
    let classes: HashMap<EntityId, &Entity> = entities
        .iter()
        .filter(|e| e.kind == EntityKind::Class)
        .map(|e| (e.id, e))
        .collect();

    let methods: HashMap<EntityId, &Entity> = entities
        .iter()
        .filter(|e| e.kind == EntityKind::Method)
        .map(|e| (e.id, e))
        .collect();

    // Build class -> methods map (methods grouped by parent class)
    let class_methods: HashMap<EntityId, HashMap<&str, EntityId>> = {
        let mut map: HashMap<EntityId, HashMap<&str, EntityId>> = HashMap::new();
        for (method_id, method) in &methods {
            if let Some(parent_id) = method.parent_id {
                if classes.contains_key(&parent_id) {
                    map.entry(parent_id)
                        .or_default()
                        .insert(&method.name, *method_id);
                }
            }
        }
        map
    };

    // Build inheritance map from Extend deps
    let inheritance: HashMap<EntityId, Vec<EntityId>> = {
        let mut map: HashMap<EntityId, Vec<EntityId>> = HashMap::new();
        for dep in deps {
            if dep.kind == DepKind::Extend {
                map.entry(dep.src).or_default().push(dep.tgt);
            }
        }
        map
    };

    // Group entities by content_id for file-based processing
    let entities_by_content: HashMap<ContentId, Vec<&Entity>> = {
        let mut map: HashMap<ContentId, Vec<&Entity>> = HashMap::new();
        for entity in entities {
            map.entry(entity.content_id).or_default().push(entity);
        }
        map
    };

    // Determine language per file
    let lang_by_content: HashMap<ContentId, Lang> = entities_by_content
        .iter()
        .filter_map(|(content_id, ents)| {
            let file_entity = ents.iter().find(|e| e.kind == EntityKind::File)?;
            let lang = Lang::of(&file_entity.name)?;
            Some((*content_id, lang))
        })
        .collect();

    // First pass: Collect ALL abstract methods across all Python files
    // Maps class_id -> set of abstract method names
    let mut abstract_methods_by_class: HashMap<EntityId, HashSet<String>> = HashMap::new();

    for (content_id, file_entities) in &entities_by_content {
        let lang = match lang_by_content.get(content_id) {
            Some(l) => *l,
            None => continue,
        };

        if lang != Lang::Python {
            continue;
        }

        let content = match reader.read(*content_id) {
            Ok(c) => c,
            Err(_) => continue,
        };

        let abstract_methods = find_python_abstract_methods(&content);
        if abstract_methods.is_empty() {
            continue;
        }

        // Map these to class entities in this file
        for entity in file_entities.iter() {
            if entity.kind != EntityKind::Class {
                continue;
            }

            // Check if this class has any of the abstract methods
            if let Some(methods_map) = class_methods.get(&entity.id) {
                for method_name in &abstract_methods {
                    if methods_map.contains_key(method_name.as_str()) {
                        abstract_methods_by_class
                            .entry(entity.id)
                            .or_default()
                            .insert(method_name.clone());
                    }
                }
            }
        }
    }

    // Now detect overrides
    let mut overrides = Vec::new();
    let mut seen: HashSet<(EntityId, EntityId)> = HashSet::new();

    // Python: For each class with Extend deps, check if it overrides abstract methods
    for (&child_class_id, _) in &classes {
        let child_methods = match class_methods.get(&child_class_id) {
            Some(m) => m,
            None => continue,
        };

        // Get all ancestors
        let mut visited = HashSet::new();
        let all_ancestors = build_all_ancestors(child_class_id, &inheritance, &mut visited);

        for ancestor_id in all_ancestors {
            // Check if ancestor has abstract methods
            let ancestor_abstract = match abstract_methods_by_class.get(&ancestor_id) {
                Some(m) => m,
                None => continue,
            };

            let ancestor_methods = match class_methods.get(&ancestor_id) {
                Some(m) => m,
                None => continue,
            };

            // For each abstract method in ancestor
            for abstract_method_name in ancestor_abstract {
                if let Some(&child_method_id) = child_methods.get(abstract_method_name.as_str()) {
                    if let Some(&ancestor_method_id) = ancestor_methods.get(abstract_method_name.as_str()) {
                        // Don't create override from a class to itself
                        if child_class_id == ancestor_id {
                            continue;
                        }

                        let edge = (child_method_id, ancestor_method_id);
                        if !seen.contains(&edge) {
                            seen.insert(edge);
                            overrides.push(Dep::new(
                                child_method_id,
                                ancestor_method_id,
                                DepKind::Override,
                                PartialPosition::Row(0),
                                PseudoCommitId::WorkDir,
                            ));
                        }
                    }
                }
            }
        }
    }

    // Java: Process @Override annotations
    for (content_id, file_entities) in &entities_by_content {
        let lang = match lang_by_content.get(content_id) {
            Some(l) => *l,
            None => continue,
        };

        if lang != Lang::Java {
            continue;
        }

        let content = match reader.read(*content_id) {
            Ok(c) => c,
            Err(_) => continue,
        };

        let override_methods = find_java_override_methods(&content);
        detect_java_overrides(
            &override_methods,
            &class_methods,
            &inheritance,
            file_entities,
            &mut seen,
            &mut overrides,
        );
    }

    overrides
}

/// Find methods with @abstractmethod decorator in Python code.
/// Returns set of method names that are abstract.
fn find_python_abstract_methods(content: &str) -> HashSet<String> {
    let mut abstract_methods = HashSet::new();

    let language = Lang::Python.ts_language();
    let mut parser = Parser::new();
    if parser.set_language(language).is_err() {
        return abstract_methods;
    }

    let tree = match parser.parse(content, None) {
        Some(t) => t,
        None => return abstract_methods,
    };

    // Query for decorated function definitions
    let query_str = r#"
        (decorated_definition
            (decorator
                (identifier) @decorator_name)
            definition: (function_definition
                name: (identifier) @method_name))
        (decorated_definition
            (decorator
                (attribute
                    attribute: (identifier) @decorator_attr))
            definition: (function_definition
                name: (identifier) @method_name2))
    "#;

    let query = match Query::new(language, query_str) {
        Ok(q) => q,
        Err(_) => return abstract_methods,
    };

    let mut cursor = QueryCursor::new();
    let root = tree.root_node();

    let idx_decorator_name = query.capture_index_for_name("decorator_name");
    let idx_decorator_attr = query.capture_index_for_name("decorator_attr");
    let idx_method_name = query.capture_index_for_name("method_name");
    let idx_method_name2 = query.capture_index_for_name("method_name2");

    for r#match in cursor.matches(&query, root, content.as_bytes()) {
        let mut is_abstract = false;
        let mut method_name: Option<&str> = None;

        for capture in r#match.captures {
            let text = capture.node.utf8_text(content.as_bytes()).unwrap_or("");

            if Some(capture.index) == idx_decorator_name && text == "abstractmethod" {
                is_abstract = true;
            }
            if Some(capture.index) == idx_decorator_attr && text == "abstractmethod" {
                is_abstract = true;
            }
            if Some(capture.index) == idx_method_name || Some(capture.index) == idx_method_name2 {
                method_name = Some(text);
            }
        }

        if is_abstract {
            if let Some(name) = method_name {
                abstract_methods.insert(name.to_string());
            }
        }
    }

    abstract_methods
}

/// Find methods with @Override annotation in Java code.
/// Returns set of (class_name, method_name) pairs.
fn find_java_override_methods(content: &str) -> HashSet<(String, String)> {
    let mut override_methods = HashSet::new();

    let language = Lang::Java.ts_language();
    let mut parser = Parser::new();
    if parser.set_language(language).is_err() {
        return override_methods;
    }

    let tree = match parser.parse(content, None) {
        Some(t) => t,
        None => return override_methods,
    };

    // Query for methods with @Override annotation
    let query_str = r#"
        (class_declaration
            name: (identifier) @class_name
            body: (class_body
                (method_declaration
                    (modifiers
                        (marker_annotation
                            name: (identifier) @annotation))
                    name: (identifier) @method_name)))
    "#;

    let query = match Query::new(language, query_str) {
        Ok(q) => q,
        Err(_) => return override_methods,
    };

    let mut cursor = QueryCursor::new();
    let root = tree.root_node();

    let idx_class_name = query.capture_index_for_name("class_name");
    let idx_annotation = query.capture_index_for_name("annotation");
    let idx_method_name = query.capture_index_for_name("method_name");

    for r#match in cursor.matches(&query, root, content.as_bytes()) {
        let mut class_name: Option<&str> = None;
        let mut method_name: Option<&str> = None;
        let mut is_override = false;

        for capture in r#match.captures {
            let text = capture.node.utf8_text(content.as_bytes()).unwrap_or("");

            if Some(capture.index) == idx_class_name {
                class_name = Some(text);
            }
            if Some(capture.index) == idx_annotation && text == "Override" {
                is_override = true;
            }
            if Some(capture.index) == idx_method_name {
                method_name = Some(text);
            }
        }

        if is_override {
            if let (Some(cls), Some(meth)) = (class_name, method_name) {
                override_methods.insert((cls.to_string(), meth.to_string()));
            }
        }
    }

    override_methods
}

/// Build transitive list of all ancestors for a class.
fn build_all_ancestors(
    class_id: EntityId,
    inheritance: &HashMap<EntityId, Vec<EntityId>>,
    visited: &mut HashSet<EntityId>,
) -> Vec<EntityId> {
    if visited.contains(&class_id) {
        return vec![];
    }
    visited.insert(class_id);

    let mut ancestors = Vec::new();
    if let Some(parents) = inheritance.get(&class_id) {
        for parent_id in parents {
            ancestors.push(*parent_id);
            ancestors.extend(build_all_ancestors(*parent_id, inheritance, visited));
        }
    }
    ancestors
}

/// Detect Java overrides based on @Override annotation.
fn detect_java_overrides(
    override_methods: &HashSet<(String, String)>,
    class_methods: &HashMap<EntityId, HashMap<&str, EntityId>>,
    inheritance: &HashMap<EntityId, Vec<EntityId>>,
    file_entities: &[&Entity],
    seen: &mut HashSet<(EntityId, EntityId)>,
    overrides: &mut Vec<EntityDep>,
) {
    // Build class name -> id mapping for this file's classes
    let class_name_to_id: HashMap<&str, EntityId> = file_entities
        .iter()
        .filter(|e| e.kind == EntityKind::Class)
        .map(|e| (e.name.as_str(), e.id))
        .collect();

    // For each (class, method) pair with @Override
    for (class_name, method_name) in override_methods {
        let class_id = match class_name_to_id.get(class_name.as_str()) {
            Some(&id) => id,
            None => continue,
        };

        let child_methods = match class_methods.get(&class_id) {
            Some(m) => m,
            None => continue,
        };

        let child_method_id = match child_methods.get(method_name.as_str()) {
            Some(&id) => id,
            None => continue,
        };

        // Get all ancestors
        let mut visited = HashSet::new();
        let all_ancestors = build_all_ancestors(class_id, inheritance, &mut visited);

        // Find first ancestor with this method
        for ancestor_id in all_ancestors {
            let ancestor_methods = match class_methods.get(&ancestor_id) {
                Some(m) => m,
                None => continue,
            };

            if let Some(&ancestor_method_id) = ancestor_methods.get(method_name.as_str()) {
                let edge = (child_method_id, ancestor_method_id);
                if !seen.contains(&edge) {
                    seen.insert(edge);
                    overrides.push(Dep::new(
                        child_method_id,
                        ancestor_method_id,
                        DepKind::Override,
                        PartialPosition::Row(0),
                        PseudoCommitId::WorkDir,
                    ));
                }
                break; // Only link to first ancestor with this method
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_find_python_abstract_methods() {
        let content = r#"
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

    @abc.abstractmethod
    def move(self):
        pass

    def eat(self):
        print("eating")
"#;
        let abstract_methods = find_python_abstract_methods(content);
        assert!(abstract_methods.contains("speak"));
        assert!(abstract_methods.contains("move"));
        assert!(!abstract_methods.contains("eat"));
    }

    #[test]
    fn test_find_java_override_methods() {
        let content = r#"
public class Dog extends Animal {
    @Override
    public void speak() {
        System.out.println("Woof");
    }

    public void fetch() {
        System.out.println("Fetching");
    }
}
"#;
        let override_methods = find_java_override_methods(content);
        assert!(override_methods.contains(&("Dog".to_string(), "speak".to_string())));
        assert!(!override_methods.contains(&("Dog".to_string(), "fetch".to_string())));
    }
}
