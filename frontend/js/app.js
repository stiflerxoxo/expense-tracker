const API = "/api/expenses";
const $ = (id) => document.getElementById(id);
const money = (n) => Number(n).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const today = () => new Date().toISOString().slice(0, 10);

let expenses = [];

function setStatus(msg, isError = false) {
  const el = $("status");
  el.textContent = msg;
  el.classList.toggle("error", isError);
}

async function api(path = "", options = {}) {
  const res = await fetch(API + path, { headers: { "Content-Type": "application/json" }, ...options });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const detail = Array.isArray(body.detail) ? body.detail.map((d) => d.msg).join(", ") : body.detail;
    throw new Error(detail || `Request failed (${res.status})`);
  }
  return res.status === 204 ? null : res.json();
}

function text(tag, value, cls) {
  const el = document.createElement(tag);
  el.textContent = value;
  if (cls) el.className = cls;
  return el;
}

function renderSummary(s) {
  $("total").textContent = money(s.total);
  $("count").textContent = `${s.count} expense${s.count === 1 ? "" : "s"}`;
  const list = $("breakdown");
  list.replaceChildren();
  const max = Math.max(...s.by_category.map((c) => c.total), 1);
  s.by_category.forEach((c) => {
    const li = document.createElement("li");
    const bar = document.createElement("span");
    bar.className = "bar";
    const fill = document.createElement("i");
    fill.style.width = `${(c.total / max) * 100}%`;
    bar.append(fill);
    li.append(text("span", c.category), bar, text("span", money(c.total), "num"));
    list.append(li);
  });
  const filter = $("filter");
  const current = filter.value;
  filter.replaceChildren(new Option("All categories", ""));
  s.by_category.forEach((c) => filter.append(new Option(c.category, c.category)));
  filter.value = s.by_category.some((c) => c.category === current) ? current : "";
}

function renderRows() {
  const body = $("rows");
  body.replaceChildren();
  expenses.forEach((e) => {
    const tr = document.createElement("tr");
    const actions = document.createElement("td");
    const edit = text("button", "Edit", "link");
    const del = text("button", "Delete", "link del");
    edit.onclick = () => startEdit(e);
    del.onclick = () => remove(e);
    actions.append(edit, del);
    tr.append(text("td", e.expense_date), text("td", e.title), text("td", e.category), text("td", money(e.amount), "num"), actions);
    body.append(tr);
  });
  $("empty").hidden = expenses.length > 0;
}

async function load() {
  try {
    const cat = $("filter").value;
    const [list, summary] = await Promise.all([
      api(cat ? `?category=${encodeURIComponent(cat)}` : ""),
      api("/summary"),
    ]);
    expenses = list;
    renderRows();
    renderSummary(summary);
    setStatus("");
  } catch (err) {
    setStatus(err.message, true);
  }
}

function resetForm() {
  $("expense-form").reset();
  $("expense-id").value = "";
  $("date").value = today();
  $("form-title").textContent = "Add expense";
  $("save").textContent = "Add expense";
  $("cancel").hidden = true;
}

function startEdit(e) {
  $("expense-id").value = e.id;
  $("title").value = e.title;
  $("amount").value = e.amount;
  $("category").value = e.category;
  $("date").value = e.expense_date;
  $("form-title").textContent = "Edit expense";
  $("save").textContent = "Save changes";
  $("cancel").hidden = false;
  $("title").focus();
}

async function remove(e) {
  if (!confirm(`Delete "${e.title}"?`)) return;
  try {
    await api(`/${e.id}`, { method: "DELETE" });
    await load();
  } catch (err) {
    setStatus(err.message, true);
  }
}

$("expense-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const id = $("expense-id").value;
  const payload = {
    title: $("title").value.trim(),
    amount: parseFloat($("amount").value),
    category: $("category").value.trim(),
    expense_date: $("date").value,
  };
  try {
    await api(id ? `/${id}` : "", { method: id ? "PUT" : "POST", body: JSON.stringify(payload) });
    resetForm();
    await load();
  } catch (err) {
    setStatus(err.message, true);
  }
});

$("cancel").onclick = resetForm;
$("filter").onchange = load;
resetForm();
load();
