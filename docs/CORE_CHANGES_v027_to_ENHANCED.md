# NeoDepends Core Changes: v0.27 → Core-Enhanced

This document details the changes made to the NeoDepends Rust core to improve Python dependency detection, achieving closer feature parity with Java analysis.

---

## Brief Description of Core Changes

Two key features were added directly to the Rust core:

### 1. isinstance() Detection (`src/stackgraphs.rs`)
Python `isinstance(obj, ClassName)` calls are now detected as `Use` dependencies. Previously, these type-checking patterns were invisible. The fix adds a tree-sitter AST traversal that identifies when a class reference appears inside an `isinstance()` call's argument list, classifying it as architecturally significant.

### 2. Override Detection (`src/override_detection.rs` - NEW FILE)
A new 490-line module detects method overrides natively:
- **Python**: Finds `@abstractmethod` decorated methods via tree-sitter query, then matches child class methods with the same name
- **Java**: Finds `@Override` annotated methods and links them to parent class methods
- Uses existing `Extend` dependencies to build inheritance chains

Both features now run as part of the core extraction pipeline (`src/main.rs`), eliminating the need for post-processing scripts to detect these relationships.

---

## Summary of Changes

| Feature | v0.27 | Core-Enhanced | Impact |
|---------|-------|---------------|--------|
| isinstance Detection | Not detected | ✅ Detected as Use | +5 deps (Survey-Python) |
| Override Detection | Not in core | ✅ Native detection | +26 deps (Survey-Python) |
| Dependency Classification | Basic | ✅ Context-aware | Improved accuracy |

---

## 1. isinstance() Detection

### Problem (v0.27)
Python `isinstance(obj, ClassName)` checks were not being detected as dependencies. This meant type-checking relationships were invisible to architectural analysis.

### Solution (Core-Enhanced)
Added `python_in_isinstance_arg()` function in `src/stackgraphs.rs` that detects when a type reference appears inside an `isinstance()` call.

**File:** `src/stackgraphs.rs` (lines 349-373)

```rust
/// Check whether `node` sits inside an `isinstance(obj, Type)` call.
/// Returns true when the reference originated from a type-check context,
/// which is architecturally significant (Use dependency).
fn python_in_isinstance_arg(node: TsNode, src: &[u8]) -> bool {
    let mut cur = Some(node);
    while let Some(n) = cur {
        if n.kind() == "argument_list" {
            if let Some(call) = n.parent() {
                if call.kind() == "call" {
                    if let Some(func) = call.child_by_field_name("function") {
                        if func.kind() == "identifier" {
                            if let Ok(name) = func.utf8_text(src) {
                                if name == "isinstance" {
                                    return true;
                                }
                            }
                        }
                    }
                }
            }
        }
        cur = n.parent();
    }
    false
}
```

**Integration** in `classify_stackgraph_dep()` (lines 430-434):

```rust
// isinstance(obj, TypeName) — the type reference is architecturally significant.
// Classify as Use explicitly for isinstance type arguments.
if python_in_isinstance_arg(src_node, src_content.as_bytes()) {
    return DepKind::Use;
}
```

### Verification
In Survey-Python `test.py/Test/add_question`, the following isinstance checks are now detected:

| Line | Code | Target Class | Dep Type |
|------|------|--------------|----------|
| 85 | `isinstance(question, (ShortAnswerQuestion, ValidDateQuestion, MultipleChoiceQuestion))` | 3 classes | Use |
| 90 | `isinstance(question, MultipleChoiceQuestion)` | MultipleChoiceQuestion | Use |
| 128 | `isinstance(question, MatchingQuestion)` | MatchingQuestion | Use |

**Total: 5 isinstance Use dependencies detected**

---

## 2. Override Detection

### Problem (v0.27)
Python method overrides (implementing `@abstractmethod` decorated methods) were not detected. Java `@Override` annotations were also not processed in the core.

### Solution (Core-Enhanced)
Added new module `src/override_detection.rs` that:

1. Parses Python files to find `@abstractmethod` decorated methods
2. Parses Java files to find `@Override` annotated methods
3. Builds inheritance chains from existing `Extend` dependencies
4. Creates `Override` dependencies from child methods to parent abstract methods

**File:** `src/override_detection.rs` (490 lines)

Key functions:
- `detect_overrides()` - Main entry point
- `find_python_abstract_methods()` - Tree-sitter query for `@abstractmethod`
- `find_java_override_methods()` - Tree-sitter query for `@Override`
- `build_all_ancestors()` - Transitive inheritance chain builder

**Integration** in `src/main.rs` (lines 372-385):

```rust
// Collect deps for override detection
let deps: Vec<_> = extractor.extract_deps(&structure_filespec).collect();

// Detect override dependencies
let entities: Vec<_> = extractor.extract_entities(&structure_filespec).collect();
let override_deps = override_detection::detect_overrides(&entities, &deps, &fs);

// Write all deps
for dep in deps {
    writer.write_dep(dep).unwrap();
}
for dep in override_deps {
    writer.write_dep(dep).unwrap();
}
```

### Verification
In Survey-Python, 26 Override dependencies are detected:

| Child Class | Parent Class | Methods Overridden |
|-------------|--------------|-------------------|
| EssayQuestion | Question | display, display_tabulation, is_valid_answer, modify_question, obtain_user_response, tabulate |
| MatchingQuestion | Question | (same 6 methods) |
| MultipleChoiceQuestion | Question | (same 6 methods) |
| ValidDateQuestion | Question | (same 6 methods) |
| ShortAnswerQuestion | Question | display_tabulation |
| TrueFalseQuestion | Question | modify_question |

---

## 3. Dependency Classification Improvements

### Context-Aware Classification
The `classify_stackgraph_dep()` function now performs context-aware classification:

```rust
// Order of checks in classify_stackgraph_dep():
1. Extend - class inheritance (class Foo(Bar))
2. isinstance Use - type checking context  [NEW]
3. Create - constructor calls (ClassName())
4. Call - function/method calls
5. Use - default for other references
```

### Design Decision: No Import Dependencies
The core intentionally does NOT create `DepKind::Import` dependencies:

```rust
// Note: We intentionally don't classify imports as DepKind::Import.
// Instead, we let them resolve to their actual usage type (Use, Call, Create, Extend)
// which is more meaningful for architectural analysis like god class decomposition.
```

**Rationale:** Entity-level dependencies (Method→Class, Class→Class) are more architecturally meaningful than file-level import statements. The actual usage pattern (Use, Call, Create, Extend) provides richer information.

---

## 4. Post-Processing (Still Required)

While the core now handles isinstance and override detection natively, some post-processing is still beneficial:

| Post-Processing Step | Purpose | Recommendation |
|---------------------|---------|----------------|
| `enhance_python_deps.py` | Prune noisy Create deps from StackGraphs | Keep enabled |
| `enhance_python_deps.py` | Add File→File Import deps | Optional |
| `enhance_python_deps.py` | Add Method→Field Use deps | Keep enabled |
| `detect_overrides.py` | Override detection | **Disable** (now in core, script creates duplicates) |

### Recommended Pipeline Flags
```bash
# Use post-processing for quality cleanup, but note override detection is now native
python3 tools/neodepends_python_export.py \
  --neodepends-bin ./target/release/neodepends \
  --input <repo> \
  --output-dir <output> \
  --langs python \
  --resolver stackgraphs \
  --dv8-hierarchy structured \
  --filter-architecture
```

---

## 5. Comparison: Raw Output

### Dependency Counts (Survey-Python)

| Dep Type | v0.27 Raw | Core-Enhanced Raw | Change |
|----------|-----------|-------------------|--------|
| Call | ~1187 | 1200 | +13 |
| Create | ~485 | 485 | - |
| Extend | 20 | 20 | - |
| Override | 0 | 26 | **+26** |
| Use | ~1118 | 1137 | +19 |
| **Total** | ~2810 | **2868** | **+58** |

### After Post-Processing (Final Output)

| Dep Type | v0.27 Final | Core-Enhanced Final | Change |
|----------|-------------|---------------------|--------|
| Call | 1606 | 1606 | - |
| Create | 61 | 61 | - |
| Extend | 29 | 29 | - |
| Import | 142 | 142 | - |
| Override | 78 | 104 | **+26** |
| Use | 1828 | 1828 | - |

---

## 6. Files Modified

| File | Changes |
|------|---------|
| `src/stackgraphs.rs` | Added `python_in_isinstance_arg()`, integrated into `classify_stackgraph_dep()` |
| `src/override_detection.rs` | **NEW** - Complete override detection module |
| `src/main.rs` | Integrated override detection into extraction pipeline |
| `src/lib.rs` | Export override_detection module |

---

## 7. Testing

### Verification Commands

```bash
# Run analysis without post-processing to see core output
python3 tools/neodepends_python_export.py \
  --neodepends-bin ./target/release/neodepends \
  --input /path/to/Survey-Python \
  --output-dir /tmp/test-core \
  --langs python \
  --resolver stackgraphs \
  --no-enhance \
  --no-override

# Check isinstance deps
sqlite3 /tmp/test-core/data/*.raw.db "
SELECT s.name, t.name
FROM deps d
JOIN entities s ON d.src = s.id
JOIN entities t ON d.tgt = t.id
WHERE d.kind = 'Use'
  AND s.name = 'add_question'
  AND t.kind = 'Class'
"

# Check override deps
sqlite3 /tmp/test-core/data/*.raw.db "
SELECT COUNT(*) FROM deps WHERE kind = 'Override'
"
# Expected: 26
```

---

## 8. Known Limitations

1. **StackGraphs Create Noise**: The core still produces ~450 noisy Create dependencies that require post-processing cleanup. These are type references misclassified as constructor calls.

2. **File→File Import deps**: Not generated by core (by design). Available via post-processing if needed.

3. **Method→Field Use deps**: Self.field patterns require post-processing for complete detection.

---

## 9. Version Information

- **Base Version**: 0.27
- **Enhanced Version**: 0.0.13 (core-enhanced)
- **Date**: February 2026
- **Rust Toolchain**: stable

---

## 10. Contributors

Core changes implemented to achieve Python/Java feature parity for dependency analysis.
