const CHATBOT_DATA = {
  project: {
    title: "Project 1: Rule-Based AI Chatbot",
    source: "Artificial intelligence P1.pdf",
    goal: "Create a simple rule-based chatbot that responds to predefined user inputs.",
    requirements: [
      "Handle greetings and exit commands",
      "Use if-else logic for responses",
      "Run in a continuous loop"
    ],
    skills: [
      "Control flow",
      "Decision-making logic",
      "Basic AI concepts"
    ]
  },
  analytics: {
    source: "Dataset for Data Analytics.xlsx",
    rows: 1200,
    dateRange: ["2023-01-01", "2025-06-30"],
    totalRevenue: 1264761.96,
    avgOrderValue: 1053.97,
    uniqueCustomers: 1189,
    products: {
      Printer: 181,
      Tablet: 179,
      Chair: 178,
      Laptop: 173,
      Desk: 170,
      Monitor: 163,
      Phone: 156
    },
    statusCounts: {
      Cancelled: 250,
      Returned: 247,
      Pending: 237,
      Shipped: 235,
      Delivered: 231
    },
    paymentMethods: {
      Online: 258,
      Cash: 246,
      "Credit Card": 234,
      "Debit Card": 232,
      "Gift Card": 230
    },
    coupons: {
      FREESHIP: 313,
      WINTER15: 292,
      SAVE10: 286
    },
    referrals: {
      Instagram: 259,
      Email: 250,
      Google: 241,
      Facebook: 228,
      Referral: 222
    },
    topRevenueProducts: {
      Chair: 195620.11,
      Printer: 195612.61,
      Laptop: 192126.56,
      Tablet: 186568.95,
      Monitor: 175651.41,
      Desk: 167459.93,
      Phone: 151722.39
    },
    sampleOrders: [
      {
        orderId: "ORD200000",
        date: "2023-01-04",
        product: "Monitor",
        quantity: 5,
        status: "Shipped",
        paymentMethod: "Debit Card",
        couponCode: "SAVE10",
        referralSource: "Instagram",
        totalPrice: 2853.10,
        trackingNumber: "TRK37947903"
      },
      {
        orderId: "ORD200001",
        date: "2024-08-23",
        product: "Phone",
        quantity: 2,
        status: "Shipped",
        paymentMethod: "Online",
        couponCode: "SAVE10",
        referralSource: "Referral",
        totalPrice: 302.70,
        trackingNumber: "TRK91186779"
      },
      {
        orderId: "ORD200002",
        date: "2024-02-27",
        product: "Tablet",
        quantity: 5,
        status: "Cancelled",
        paymentMethod: "Credit Card",
        couponCode: "FREESHIP",
        referralSource: "Email",
        totalPrice: 2753.40,
        trackingNumber: "TRK42903982"
      }
    ]
  }
};
