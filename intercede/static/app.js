const KEY = "intercede.prayerList";
const $ = (id) => document.getElementById(id);

function load() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; } }
function save(list) { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch {} }

function el(tag, text, cls) {
  const n = document.createElement(tag);
  if (text) n.textContent = text;
  if (cls) n.className = cls;
  return n;
}

function card(story, btnLabel, onClick) {
  const c = el("article", "", "card");
  c.append(el("span", story.category + "", "cat"), el("h3", story.title));
  const ul = el("ul");
  story.prayer_points.forEach((p) => ul.append(el("li", p)));
  const a = el("a", "Read the article");
  a.href = story.url; a.target = "_blank"; a.rel = "noopener";
  const b = el("button", btnLabel);
  b.addEventListener("click", () => onClick(story));
  c.append(ul, el("p", story.source, "meta"), a, document.createTextNode(" "), b);
  return c;
}

function renderList() {
  const box = $("list"); box.replaceChildren();
  const list = load();
  if (!list.length) box.append(el("p", "Nothing saved yet.", "meta"));
  list.forEach((s) => box.append(card(s, "Remove", (x) => {
    save(load().filter((i) => i.id !== x.id)); renderList();
  })));
}

async function loadStories() {
  const [city, country] = $("city").value.split("|");
  $("status").textContent = "Loading…";
  $("stories").replaceChildren();
  try {
    const r = await fetch(`/api/stories?city=${encodeURIComponent(city)}&country=${encodeURIComponent(country)}`);
    const data = await r.json();
    if (!r.ok) { $("status").textContent = data.error || "Something went wrong."; return; }
    $("status").textContent = data.length ? "" : "No stories need prayer here right now.";
    data.forEach((s) => $("stories").append(card(s, "Pray", (x) => {
      const l = load();
      if (!l.some((i) => i.id === x.id)) { l.push(x); save(l); }
      renderList();
    })));
  } catch { $("status").textContent = "Could not reach the server."; }
}

$("city").addEventListener("change", loadStories);
renderList(); loadStories();
