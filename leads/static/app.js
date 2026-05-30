let leadsData = [];

function handleSearch() {
  const query = document.getElementById("query").value.trim();
  if (!query) return;
  search(query);
}

document.getElementById("query").addEventListener("keydown", function (e) {
  if (e.key === "Enter") handleSearch();
});

async function search(query) {
  leadsData = [];
  setSearching(true);
  hideResults();
  showStatus("info", "Fetching results from Google Places…");

  let data;
  try {
    const resp = await fetch("/api/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    data = await resp.json();
  } catch (e) {
    showStatus("error", "Network error: " + e.message);
    setSearching(false);
    return;
  }

  if (data.error) {
    showStatus("error", "Google API error: " + data.error + " (" + data.status + ")");
    setSearching(false);
    return;
  }

  if (data.status === "ZERO_RESULTS" || data.count === 0) {
    showStatus("info", "No results found for that query. Try a different search.");
    setSearching(false);
    return;
  }

  renderTable(data.places);
  showStatus("info", "Enriching " + data.places.length + " results with contact details…", true);

  await enrichDetails(data.places);

  hideStatus();
  setSearching(false);
}

function renderTable(places) {
  const tbody = document.getElementById("results-body");
  tbody.innerHTML = "";

  places.forEach((place) => {
    const tr = document.createElement("tr");
    tr.dataset.placeId = place.place_id;

    tr.innerHTML =
      '<td class="name">' + esc(place.name) + "</td>" +
      '<td class="address">' + esc(place.address) + "</td>" +
      '<td class="phone"><span class="loading">Loading…</span></td>' +
      '<td class="website"><span class="loading">Loading…</span></td>' +
      '<td class="rating">' + ratingHtml(place.rating) + "</td>" +
      '<td class="maps"><span class="loading">Loading…</span></td>';

    tbody.appendChild(tr);

    leadsData.push({
      name: place.name,
      address: place.address,
      rating: place.rating != null ? place.rating : "",
      phone: "",
      website: "",
      maps_url: "",
      place_id: place.place_id,
    });
  });

  document.getElementById("results-count").textContent =
    places.length + " business" + (places.length === 1 ? "" : "es") + " found";
  document.getElementById("results-panel").classList.remove("hidden");
  document.getElementById("csv-btn").classList.add("hidden");
}

async function enrichDetails(places) {
  const place_ids = places.map((p) => p.place_id);

  let details;
  try {
    const resp = await fetch("/api/details", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ place_ids }),
    });
    details = await resp.json();
  } catch (e) {
    return;
  }

  places.forEach((place) => {
    const d = details[place.place_id] || {};
    const tr = document.querySelector('tr[data-place-id="' + place.place_id + '"]');
    if (!tr) return;

    const cells = tr.querySelectorAll("td");

    // Phone
    cells[2].textContent = d.phone || "—";

    // Website
    if (d.website) {
      let domain;
      try {
        domain = new URL(d.website).hostname.replace(/^www\./, "");
      } catch (_) {
        domain = d.website;
      }
      cells[3].innerHTML =
        '<a href="' + esc(d.website) + '" target="_blank" rel="noopener" class="website-text" title="' + esc(d.website) + '">' +
        esc(domain) + "</a>";
    } else {
      cells[3].textContent = "—";
    }

    // Maps
    if (d.maps_url) {
      cells[5].innerHTML =
        '<a href="' + esc(d.maps_url) + '" target="_blank" rel="noopener" class="maps-link">View ↗</a>';
    } else {
      cells[5].textContent = "—";
    }

    // Update leadsData entry
    const entry = leadsData.find((x) => x.place_id === place.place_id);
    if (entry) {
      entry.phone = d.phone || "";
      entry.website = d.website || "";
      entry.maps_url = d.maps_url || "";
    }
  });

  document.getElementById("csv-btn").classList.remove("hidden");
}

function downloadCSV() {
  const header = ["Name", "Address", "Phone", "Website", "Rating", "Maps URL"];
  const rows = leadsData.map((d) => [
    d.name, d.address, d.phone, d.website,
    d.rating != null ? d.rating : "",
    d.maps_url,
  ]);

  const csv = [header, ...rows]
    .map((row) =>
      row.map((cell) => {
        const s = String(cell == null ? "" : cell);
        return s.includes(",") || s.includes('"') || s.includes("\n")
          ? '"' + s.replace(/"/g, '""') + '"'
          : s;
      }).join(",")
    )
    .join("\r\n");

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "leads.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function showStatus(type, message, spinner) {
  const bar = document.getElementById("status-bar");
  bar.className = type;
  bar.innerHTML = (spinner ? '<div class="spinner"></div>' : "") + "<span>" + esc(message) + "</span>";
  bar.classList.remove("hidden");
}

function hideStatus() {
  document.getElementById("status-bar").classList.add("hidden");
}

function hideResults() {
  document.getElementById("results-panel").classList.add("hidden");
  document.getElementById("results-body").innerHTML = "";
}

function setSearching(on) {
  document.getElementById("search-btn").disabled = on;
}

function ratingHtml(rating) {
  if (rating == null) return "—";
  return '<span class="star">&#9733;</span> ' + rating.toFixed(1);
}

function esc(str) {
  return String(str == null ? "" : str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
