const messages = document.querySelector("#messages");
const form = document.querySelector("#chat-form");
const input = document.querySelector("#chat-input");
const chips = document.querySelectorAll("[data-prompt]");

const data = CHATBOT_DATA;

function currency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(value);
}

function listFromObject(object, formatter = (key, value) => `${key}: ${value}`) {
  return Object.entries(object).map(([key, value]) => formatter(key, value)).join("<br>");
}

function addMessage(text, sender = "bot", note = "") {
  const message = document.createElement("div");
  message.className = `message ${sender}`;
  message.innerHTML = `${text}${note ? `<small>${note}</small>` : ""}`;
  messages.appendChild(message);
  messages.scrollTop = messages.scrollHeight;
}

function findOrder(text) {
  const upper = text.toUpperCase();
  return data.analytics.sampleOrders.find((order) => upper.includes(order.orderId));
}

function replyTo(rawText) {
  const text = rawText.toLowerCase().trim();
  const order = findOrder(rawText);

  if (!text) {
    return "Drop a message first and I will match it with my rule engine.";
  } else if (text.includes("bye") || text.includes("exit") || text.includes("quit") || text.includes("stop")) {
    return "Session closed in style. Type hello whenever you want to restart the loop.";
  } else if (text.includes("hello") || text.includes("hi") || text.includes("hey") || text.includes("namaste")) {
    return "Hey, I am NovaBot. I use rule-based if-else logic and the linked project data to answer your questions.";
  } else if (text.includes("help") || text.includes("what can you do")) {
    return "I can answer about the project goal, requirements, dataset size, revenue, products, order status, payment methods, coupons, referrals, and sample order tracking.";
  } else if (text.includes("goal") || text.includes("project")) {
    return `${data.project.title}<br>${data.project.goal}<br><br>Key requirements:<br>${data.project.requirements.join("<br>")}`;
  } else if (text.includes("skill")) {
    return `This project builds: ${data.project.skills.join(", ")}.`;
  } else if (text.includes("dataset") || text.includes("data")) {
    return `The linked dataset has ${data.analytics.rows.toLocaleString()} orders, ${data.analytics.uniqueCustomers.toLocaleString()} unique customers, and covers ${data.analytics.dateRange[0]} to ${data.analytics.dateRange[1]}.`;
  } else if (text.includes("revenue") || text.includes("sales") || text.includes("total")) {
    return `Total revenue is ${currency(data.analytics.totalRevenue)}. Average order value is ${currency(data.analytics.avgOrderValue)}.`;
  } else if (text.includes("product") || text.includes("items")) {
    return `Product counts:<br>${listFromObject(data.analytics.products)}<br><br>Top revenue products:<br>${listFromObject(data.analytics.topRevenueProducts, (key, value) => `${key}: ${currency(value)}`)}`;
  } else if (text.includes("status") || text.includes("delivered") || text.includes("cancelled") || text.includes("pending") || text.includes("returned") || text.includes("shipped")) {
    return `Order status breakdown:<br>${listFromObject(data.analytics.statusCounts)}`;
  } else if (text.includes("payment") || text.includes("cash") || text.includes("card") || text.includes("online")) {
    return `Payment method usage:<br>${listFromObject(data.analytics.paymentMethods)}`;
  } else if (text.includes("coupon") || text.includes("discount") || text.includes("save10") || text.includes("freeship") || text.includes("winter15")) {
    return `Coupon code usage:<br>${listFromObject(data.analytics.coupons)}`;
  } else if (text.includes("referral") || text.includes("source") || text.includes("instagram") || text.includes("email") || text.includes("google") || text.includes("facebook")) {
    return `Referral sources:<br>${listFromObject(data.analytics.referrals)}`;
  } else if (order || text.includes("tracking") || text.includes("sample order")) {
    const selected = order || data.analytics.sampleOrders[0];
    return `Sample order ${selected.orderId}: ${selected.product}, quantity ${selected.quantity}, status ${selected.status}, paid by ${selected.paymentMethod}, total ${currency(selected.totalPrice)}, tracking ${selected.trackingNumber}.`;
  } else if (text.includes("source") || text.includes("linked")) {
    return `I am linked to ${data.project.source} for project rules and ${data.analytics.source} for analytics facts.`;
  } else {
    return "I do not have that rule yet. Try asking about revenue, products, status, payment, coupons, referrals, project goal, or say exit.";
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = input.value;
  addMessage(text, "user");
  input.value = "";
  window.setTimeout(() => addMessage(replyTo(text), "bot", "Rule matched with if-else logic"), 220);
});

chips.forEach((chip) => {
  chip.addEventListener("click", () => {
    input.value = chip.dataset.prompt;
    form.requestSubmit();
  });
});

addMessage("Hello. I am NovaBot, your rule-based AI chatbot powered by the linked Excel and PDF project data.", "bot", "Ready");
