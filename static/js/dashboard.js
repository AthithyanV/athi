/* Dashboard real-time logic */
document.addEventListener("DOMContentLoaded", function () {
    const socket = io();

    let batches = [];
    let buyers = [];
    let slots = [];

    /* ---- Socket events ---- */
    socket.on("connect", function () {
        document.getElementById("conn-status").textContent = "Connected";
    });
    socket.on("disconnect", function () {
        document.getElementById("conn-status").textContent = "Disconnected";
    });
    socket.on("batch_update", function (data) {
        batches = data.batches;
        renderBatches();
        refreshStats();
    });
    socket.on("buyer_update", function (data) {
        buyers = data.buyers;
        renderBuyers();
        refreshStats();
    });
    socket.on("slot_update", function (data) {
        slots = data.slots;
        renderSlots();
        refreshStats();
    });

    /* ---- API helpers ---- */
    function api(method, url, body) {
        var opts = { method: method, headers: { "Content-Type": "application/json" } };
        if (body) opts.body = JSON.stringify(body);
        return fetch(url, opts).then(function (r) { return r.json(); });
    }

    /* ---- Batch form ---- */
    document.getElementById("batch-form").addEventListener("submit", function (e) {
        e.preventDefault();
        var f = e.target;
        api("POST", "/api/batches", {
            variety: f.variety.value,
            weight_kg: parseFloat(f.weight_kg.value),
            moisture_pct: parseFloat(f.moisture_pct.value),
            origin: f.origin.value,
        }).then(function () { toast("Batch created with AI prediction"); f.reset(); });
    });

    /* ---- Buyer form ---- */
    document.getElementById("buyer-form").addEventListener("submit", function (e) {
        e.preventDefault();
        var f = e.target;
        api("POST", "/api/buyers", {
            name: f.buyer_name.value,
            company: f.company.value,
            preferred_varieties: f.pref_varieties.value.split(",").map(function (v) { return v.trim(); }),
            max_quantity_kg: parseFloat(f.max_qty.value),
        }).then(function () { toast("Buyer registered"); f.reset(); });
    });

    /* ---- Render tables ---- */
    function renderBatches() {
        var tb = document.getElementById("batches-body");
        tb.innerHTML = "";
        batches.forEach(function (b) {
            var gradeClass = { "A+": "badge-green", "A": "badge-blue", "B+": "badge-yellow", "B": "badge-yellow", "C": "badge-red" };
            var tr = document.createElement("tr");
            tr.innerHTML =
                "<td>" + b.id + "</td>" +
                "<td>" + b.variety + "</td>" +
                "<td>" + b.weight_kg + "</td>" +
                "<td>" + b.moisture_pct + "%</td>" +
                "<td><span class='badge badge-purple'>" + b.current_stage + "</span></td>" +
                "<td><span class='badge " + (gradeClass[b.predicted_grade] || "badge-blue") + "'>" + (b.predicted_grade || "-") + "</span></td>" +
                "<td><span class='badge " + (gradeClass[b.quality_grade] || "") + "'>" + (b.quality_grade || "-") + "</span></td>" +
                "<td>" +
                    "<button class='btn btn-sm btn-primary' onclick='advanceBatch(\"" + b.id + "\")'>Next</button> " +
                    "<button class='btn btn-sm btn-success' onclick='autoAllocate(\"" + b.id + "\")'>Allocate</button>" +
                "</td>";
            tb.appendChild(tr);
        });
    }

    function renderBuyers() {
        var tb = document.getElementById("buyers-body");
        tb.innerHTML = "";
        buyers.forEach(function (b) {
            var tr = document.createElement("tr");
            tr.innerHTML =
                "<td>" + b.id + "</td>" +
                "<td>" + b.name + "</td>" +
                "<td>" + b.company + "</td>" +
                "<td>" + b.preferred_varieties.join(", ") + "</td>" +
                "<td>" + b.remaining_capacity_kg + " / " + b.max_quantity_kg + "</td>";
            tb.appendChild(tr);
        });
    }

    function renderSlots() {
        var tb = document.getElementById("slots-body");
        tb.innerHTML = "";
        slots.forEach(function (s) {
            var statusClass = { Pending: "badge-yellow", Confirmed: "badge-blue", Delivered: "badge-green" };
            var tr = document.createElement("tr");
            tr.innerHTML =
                "<td>" + s.id + "</td>" +
                "<td>" + s.batch_id + "</td>" +
                "<td>" + s.buyer_id + "</td>" +
                "<td>" + s.allocated_kg + " kg</td>" +
                "<td>" + s.variety + "</td>" +
                "<td><span class='badge " + (statusClass[s.status] || "") + "'>" + s.status + "</span></td>" +
                "<td>" + s.score + "</td>" +
                "<td>" +
                    (s.status === "Pending" ? "<button class='btn btn-sm btn-primary' onclick='confirmSlot(\"" + s.id + "\")'>Confirm</button> " : "") +
                    (s.status === "Confirmed" ? "<button class='btn btn-sm btn-success' onclick='deliverSlot(\"" + s.id + "\")'>Deliver</button>" : "") +
                "</td>";
            tb.appendChild(tr);
        });
    }

    /* ---- Stats ---- */
    function refreshStats() {
        api("GET", "/api/dashboard/stats").then(function (d) {
            document.getElementById("stat-batches").textContent = d.total_batches;
            document.getElementById("stat-buyers").textContent = d.total_buyers;
            document.getElementById("stat-allocated").textContent = d.total_allocated_kg + " kg";
            document.getElementById("stat-alloc-pct").textContent = d.allocation_pct + "%";
            document.getElementById("stat-slots").textContent = d.total_slots;
            document.getElementById("stat-weight").textContent = d.total_weight_kg + " kg";
            renderChart("stage-chart", d.stage_distribution, "var(--primary)");
            renderChart("grade-chart", d.grade_distribution, "#16a34a");
        });
    }

    function renderChart(containerId, data, color) {
        var el = document.getElementById(containerId);
        el.innerHTML = "";
        var keys = Object.keys(data);
        if (keys.length === 0) { el.innerHTML = "<span style='color:var(--text-light);font-size:.8rem'>No data yet</span>"; return; }
        var maxVal = Math.max.apply(null, keys.map(function (k) { return data[k]; }));
        keys.forEach(function (k) {
            var pct = maxVal > 0 ? (data[k] / maxVal) * 100 : 0;
            var bar = document.createElement("div");
            bar.className = "chart-bar";
            bar.style.height = Math.max(pct, 5) + "%";
            bar.style.background = color;
            bar.innerHTML = "<span class='chart-value'>" + data[k] + "</span><span class='chart-label'>" + k + "</span>";
            el.appendChild(bar);
        });
    }

    /* ---- Toast ---- */
    function toast(msg) {
        var t = document.getElementById("toast");
        t.textContent = msg;
        t.classList.add("show");
        setTimeout(function () { t.classList.remove("show"); }, 2500);
    }

    /* ---- Global action handlers ---- */
    window.advanceBatch = function (id) {
        api("POST", "/api/batches/" + id + "/advance").then(function () { toast("Stage advanced"); });
    };
    window.autoAllocate = function (id) {
        api("POST", "/api/slots/auto-allocate/" + id).then(function (r) {
            if (r.error) { toast("Error: " + r.error); } else { toast("Allocated to buyer " + r.buyer_id); }
        });
    };
    window.confirmSlot = function (id) {
        api("POST", "/api/slots/" + id + "/confirm").then(function () { toast("Slot confirmed"); });
    };
    window.deliverSlot = function (id) {
        api("POST", "/api/slots/" + id + "/deliver").then(function () { toast("Slot delivered"); });
    };

    /* Initial data load */
    refreshStats();
});
