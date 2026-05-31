let leadsData = [];

function handleSearch() {
  const query = document.getElementById("query").value.trim();
  if (!query) {
    document.getElementById("query").focus();
    return;
  }
  search(query);
}

document.getElementById("query").addEventListener("keydown", function (e) {
  if (e.key === "Enter") handleSearch();
});

async function search(query) {
  leadsData = [];
  setSearching(true);
  hideEmpty();
  hideResults();
  showStatus("info", "Searching Google Places…", true);

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
    const detail = data.status && data.status !== data.error
      ? data.error + " (" + data.status + ")"
      : data.error;
    showStatus("error", "Google API error: " + detail);
    setSearching(false);
    return;
  }

  if (data.status === "ZERO_RESULTS" || data.count === 0) {
    showStatus("info", "No results found. Try a different location or business type.");
    setSearching(false);
    return;
  }

  renderSkeleton(data.places);
  showStatus("info", "Fetching contact details for " + data.places.length + " businesses…", true);

  await enrichDetails(data.places);

  hideStatus();
  setSearching(false);
}

function renderSkeleton(places) {
  const tbody = document.getElementById("results-body");
  tbody.innerHTML = "";
  leadsData = [];

  places.forEach((place) => {
    const tr = document.createElement("tr");
    tr.dataset.placeId = place.place_id;

    tr.innerHTML =
      '<td class="name">' + esc(place.name) + "</td>" +
      '<td class="address">' + esc(place.address) + "</td>" +
      '<td class="phone"><span class="skel" style="width:' + skelW(72, 118) + 'px" aria-label="Loading"></span></td>' +
      '<td class="website"><span class="skel" style="width:' + skelW(55, 105) + 'px" aria-label="Loading"></span></td>' +
      '<td class="rating">' + ratingHtml(place.rating) + "</td>" +
      '<td class="maps"><span class="skel" style="width:38px" aria-label="Loading"></span></td>';

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

  const count = places.length;
  document.getElementById("results-count").textContent =
    count + " result" + (count === 1 ? "" : "s");
  document.getElementById("csv-btn").classList.add("hidden");
  document.getElementById("results-panel").classList.remove("hidden");
}

function skelW(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
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
  } catch (_) {
    details = {};
  }

  places.forEach((place) => {
    const d = details[place.place_id] || {};
    const tr = document.querySelector('tr[data-place-id="' + place.place_id + '"]');
    if (!tr) return;

    const cells = tr.querySelectorAll("td");

    // Phone
    cells[2].innerHTML = d.phone
      ? esc(d.phone)
      : '<span class="null-dash">—</span>';

    // Website
    if (d.website) {
      let domain;
      try { domain = new URL(d.website).hostname.replace(/^www\./, ""); }
      catch (_) { domain = d.website; }
      cells[3].innerHTML =
        '<a href="' + esc(d.website) + '" target="_blank" rel="noopener" class="website-link" title="' + esc(d.website) + '">' +
        esc(domain) + "</a>";
    } else {
      cells[3].innerHTML = '<span class="null-dash">—</span>';
    }

    // Maps
    if (d.maps_url) {
      cells[5].innerHTML =
        '<a href="' + esc(d.maps_url) + '" target="_blank" rel="noopener" class="maps-link">' +
        '<svg width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden="true"><path d="M2 8l6-6M3 2h5v5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
        "View</a>";
    } else {
      cells[5].innerHTML = '<span class="null-dash">—</span>';
    }

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
  bar.className = "status " + type;
  bar.innerHTML =
    (spinner ? '<div class="spinner" role="img" aria-label="Loading"></div>' : "") +
    '<span>' + esc(message) + '</span>';
  bar.classList.remove("hidden");
}

function hideStatus() {
  document.getElementById("status-bar").classList.add("hidden");
}

function hideResults() {
  document.getElementById("results-panel").classList.add("hidden");
  document.getElementById("results-body").innerHTML = "";
}

function hideEmpty() {
  document.getElementById("empty-state").classList.add("hidden");
}

function setSearching(on) {
  const btn = document.getElementById("search-btn");
  btn.disabled = on;
  btn.textContent = on ? "Searching…" : "Search";
}

function ratingHtml(rating) {
  if (rating == null) return '<span class="null-dash">—</span>';
  return (
    '<span class="rating-val">' +
    '<svg class="star-icon" width="11" height="11" viewBox="0 0 12 12" fill="currentColor" aria-hidden="true">' +
    '<path d="M6 1l1.18 2.4 2.64.38-1.91 1.86.45 2.63L6 7.05 3.64 8.27l.45-2.63L2.18 3.78l2.64-.38L6 1z"/>' +
    '</svg>' +
    rating.toFixed(1) +
    '</span>'
  );
}

function esc(str) {
  return String(str == null ? "" : str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
