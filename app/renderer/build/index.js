(() => {
  var __create = Object.create;
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __getProtoOf = Object.getPrototypeOf;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __require = /* @__PURE__ */ ((x) => typeof require !== "undefined" ? require : typeof Proxy !== "undefined" ? new Proxy(x, {
    get: (a, b) => (typeof require !== "undefined" ? require : a)[b]
  }) : x)(function(x) {
    if (typeof require !== "undefined") return require.apply(this, arguments);
    throw Error('Dynamic require of "' + x + '" is not supported');
  });
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
    // If the importer is in node compatibility mode or this is not an ESM
    // file that has been converted to a CommonJS file using a Babel-
    // compatible transform (i.e. "__esModule" has not been set), then set
    // "default" to the CommonJS "module.exports" for node compatibility.
    isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
    mod
  ));

  // app/renderer/index.jsx
  var import_react3 = __toESM(__require("react"));
  var import_react_dom = __toESM(__require("react-dom"));

  // app/renderer/components/Chat.jsx
  var import_react2 = __toESM(__require("react"));

  // app/renderer/components/MessageList.jsx
  var import_react = __toESM(__require("react"));
  function ChatMessage({ message }) {
    const { role, content } = message;
    const isUser = role === "user";
    const label = isUser ? "You" : "Gemma";
    return /* @__PURE__ */ import_react.default.createElement("div", { className: `message-wrapper ${role}` }, /* @__PURE__ */ import_react.default.createElement("div", { className: "message-label" }, label), /* @__PURE__ */ import_react.default.createElement("div", { className: `message ${role}` }, content));
  }
  function MessageList({ messages: messages2, isLoading, messagesEndRef }) {
    return /* @__PURE__ */ import_react.default.createElement("div", { className: "messages-container" }, messages2.map((msg, index) => /* @__PURE__ */ import_react.default.createElement(ChatMessage, { key: index, message: msg })), isLoading && /* @__PURE__ */ import_react.default.createElement("div", { className: "message-wrapper assistant" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "message-label" }, "Gemma"), /* @__PURE__ */ import_react.default.createElement("div", { className: "message loading" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "typing-indicator" }, /* @__PURE__ */ import_react.default.createElement("span", null), /* @__PURE__ */ import_react.default.createElement("span", null), /* @__PURE__ */ import_react.default.createElement("span", null)))), /* @__PURE__ */ import_react.default.createElement("div", { ref: messagesEndRef }));
  }
  var MessageList_default = MessageList;

  // app/renderer/components/Chat.jsx
  function Chat() {
    const [message, setMessage] = (0, import_react2.useState)("");
    const [messages2, setMessages2] = (0, import_react2.useState)([]);
    const [isLoading, setIsLoading] = (0, import_react2.useState)(false);
    const messagesEndRef = import_react2.default.useRef(null);
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };
    import_react2.default.useEffect(() => {
      scrollToBottom();
    }, [messages2]);
    const handleSubmit = async (e) => {
      e.preventDefault();
      if (!message.trim() || isLoading) return;
      const newMessage = { role: "user", content: message };
      setMessages2((prev) => [...prev, newMessage]);
      setIsLoading(true);
      try {
        const response = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ prompt: message })
        });
        const data = await response.json();
        if (response.ok) {
          ((prev) => [...prev, {
            role: "assistant",
            content: data.response,
            ...data.execution_result && {
              execution: data.execution_result
            }
          }]);
        } else {
          console.error("Error:", data);
          setMessages2((prev) => [...prev, { role: "error", content: "Failed to get response" }]);
        }
      } catch (error) {
        console.error("Error:", error);
        setMessages2((prev) => [...prev, { role: "error", content: "Network error" }]);
      } finally {
        setIsLoading(false);
        setMessage("");
      }
    };
    return /* @__PURE__ */ import_react2.default.createElement("div", { className: "chat-container" }, /* @__PURE__ */ import_react2.default.createElement("div", { className: "chat-header" }, /* @__PURE__ */ import_react2.default.createElement("h3", null, "Chat with Gemma")), /* @__PURE__ */ import_react2.default.createElement(
      MessageList_default,
      {
        messages: messages2,
        isLoading,
        messagesEndRef
      }
    ), /* @__PURE__ */ import_react2.default.createElement("form", { onSubmit: handleSubmit, className: "chat-input" }, /* @__PURE__ */ import_react2.default.createElement(
      "input",
      {
        type: "text",
        value: message,
        onChange: (e) => setMessage(e.target.value),
        placeholder: "Type your message...",
        disabled: isLoading
      }
    ), /* @__PURE__ */ import_react2.default.createElement("button", { type: "submit", disabled: isLoading }, isLoading ? "Sending..." : "Send")));
  }
  var Chat_default = Chat;

  // app/renderer/index.jsx
  function App() {
    const addTab = () => {
      const newTab = {
        id: nextTabId,
        url: "https://duckduckgo.com",
        title: "New Tab"
      };
      setTabs([...tabs, newTab]);
      setActiveTabId(nextTabId);
      setNextTabId(nextTabId + 1);
    };
    const closeTab = (tabId) => {
      if (tabs.length === 1) {
        addTab();
      }
      const newTabs = tabs.filter((tab) => tab.id !== tabId);
      setTabs(newTabs);
      if (activeTabId === tabId) {
        setActiveTabId(newTabs[newTabs.length - 1].id);
      }
    };
    const handleTabClick = (tabId) => {
      setActiveTabId(tabId);
    };
    const handlePromptChange = (event) => {
      setPrompt(event.target.value);
    };
    const handleSendPrompt = async () => {
      const response = await fetch("http://127.0.0.1:8000/agent/plan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt })
      });
      const data = await response.json();
      setMessages([...messages, { type: "user", text: prompt }, { type: "agent", text: JSON.stringify(data.plan) }]);
      const executeResponse = await fetch("http://127.0.0.1:8000/agent/execute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ plan: data.plan })
      });
      const executeData = await executeResponse.json();
      setMessages([...messages, { type: "user", text: prompt }, { type: "agent", text: JSON.stringify(data.plan) }, { type: "agent", text: JSON.stringify(executeData) }]);
    };
    return /* @__PURE__ */ import_react3.default.createElement("div", { className: "app-container" }, /* @__PURE__ */ import_react3.default.createElement(Chat_default, null));
  }
  var root = import_react_dom.default.createRoot(document.getElementById("root"));
  root.render(/* @__PURE__ */ import_react3.default.createElement(App, null));
})();
