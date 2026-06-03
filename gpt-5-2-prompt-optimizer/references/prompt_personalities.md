# Shaping your agent’s personality

Similar to ChatGPT’s built-in personality [presets](https://help.openai.com/en/articles/11899719-customizing-your-chatgpt-personality), you can steer your Agent’s behavior by explicitly defining its personality in your prompt instructions. These instructions—sometimes called the “system prompt” or “developer prompt”—guide the agent’s tone, detail level, and style of responses. In this notebook, we’ll refer to them simply as “instructions,” following the term used in the [OpenAI API documentation](https://platform.openai.com/docs/guides/text-generation/introduction) for consistency.

Defining personality at the system instructions level helps control verbosity, structure, and decision-making style across all interactions.

---

## What is agent personality? 

A personality defines the style and tone the model uses when responding. It shapes how answers feel - for example, polished and professional, concise and utilitarian, or direct and corrective.

Changing the personality influences how responses are communicated. Personalities also do not override task‑specific output formats. If you ask for an email, code snippet, JSON, or résumé, the model should follow your instructions and the task context rather than the selected personality.

**Below are example personalities for API and agent use, with sample instruction prompts you can adapt directly in your application.** The examples show that personality should not be treated as aesthetic polish, but as an operational lever that improves consistency, reduces drift, and aligns model behavior with user expectations and business constraints.

---

## Prerequisites

Before running this notebook, make sure you have installed the following packages:

---

## 1 Professional 

Polished and precise. Uses formal language and professional writing conventions.

**Best for:** Enterprise agents, legal/finance workflows, production support 

**Why it works:** Reinforces precision, business‑appropriate tone, and disciplined execution; mitigates over‑casual drift.

---

As an example, professional prompt can be used for drafting formal communication such as: **Announce a per diem of $75 in company travel reimbursement policy**

---

## 2 Efficient 

Concise and plain, delivering direct answers without extra words.

**Best for:** Code Generation, Developer tools, background agents, batch automation, evaluators, SDK‑heavy use cases.

**Why it works:** Directly counters verbosity, narration, and over‑scaffolding; aligns with token efficiency.

---

For efficient personality, let's take example of when you just need a list of ingedients for a dish: **Grocery list for cooking tomato soup**

---

## 3 Fact-Based 

Direct and encouraging, grounded answers, and clear next steps.

**Best for:** Debugging, evals, risk analysis, coaching workflows, document parsing & reviews.

**Why it works:** Encourages honest feedback, grounded responses, clamps hallucinations, explicit trade‑offs, and corrective guidance without drifting into friendliness or hedging.

---

Let's use an example where your agent needs to cite the sources. The agent will search the web to find **"How many US Federal holidays are there in the year 2026?"** 

**Note:** The use of the `web_search` tool is optional and should be included only if your use case requires searching external information. If your application does not need web access or external lookups, you can omit the `tools=[{"type": "web_search"}]` argument.

---

## 4 Exploratory

Exploratory and enthusiastic, explaining concepts clearly while celebrating knowledge and discovery.

**Best for:** Internal documentation copilot, onboarding help, technical excellence, training/enablement.

**Why it works:** Reinforces exploration and deep understanding; fosters technical curiosity and knowledge sharing within teams.

---

Let's take an example where we want the agent to explain in detail - "What is the weather usually like in San Francisco around January?"

---

## Conclusion

Agent personality is a critical lever for shaping how your system behaves in production. By defining personality instructions explicitly at the system or developer-prompt level, you can reliably steer tone, verbosity, structure, and decision-making style without interfering with task-specific instructions or output formats.

This cookbook demonstrated how different personality profiles—such as Professional, Efficient, Fact-based, and Exploratory—map cleanly to real-world use cases, from enterprise workflows and developer tooling to research assistants and internal enablement. 

In practice, the most effective approach is to start with a minimal, well-scoped personality aligned to the target workload, validate it through evals, and evolve it deliberately as requirements change. Avoid overloading personalities with task logic or domain rules—keep them focused on how the agent responds, not what it must do.

Used thoughtfully, agent personalities enable you to build systems that are not only more useful, but more predictable, scalable, and trustworthy in real production environments.
