https://steel-dev.notion.site/Reza-Jafar-Trial-Project-15b518e4524180d18f19cb9ed778755d

# Reza Jafar Trial Project

<aside>
👋

**Welcome, Reza!** Everything you need for the trial project should be covered in this document. If you have questions, feel free to reach out in your dedicated Slack channel.

</aside>

## The Project

Create a Langchain integration for Steel.dev that enables AI agents to leverage Steel for web automation tasks. Along with a cookbook example and clean documentation guide.

Reference: 

- `https://python.langchain.com/docs/integrations/tools/playwright/#use-within-an-agent`
- `https://python.langchain.com/docs/integrations/document_loaders/browserless/`
- `https://python.langchain.com/docs/contributing/`
- `https://docs.steel.dev/overview/intro-to-steel`
- `https://python.langchain.com/docs/integrations/document_loaders/browserbase/#loader-options`
- `https://docs.browserbase.com/integrations/crew-ai/build-a-flight-booker`

## Technical Requirements


### 1. Core Integration Checklist

[ ] Create a Steel loader for Langchain: 
    [ ] Loads a web page
    [ ] Implement in the Langchain loaders repository
    [ ] Follow Langchain's loader patterns and conventions
    [ ] Include proper error handling and logging
[ ] PR in the langchain community tools repo (probably as a document loader) - https://github.com/langchain-ai/langchain/tree/fa0618883493cf6a1447a73b66cd10c0f028e09b/libs/community/langchain_community/document_loaders
[ ] Must work with Self-hosted Steel and Steel Cloud
[ ] Optional (we are doing this for the crewAI integration): A loader that start and stops sessions as a core primitive for langchain devs to build tools to wrap around it.

### 2. Example Agent Implementation

- Create a code example using the Langchain x Steel for the Steel cookbooks
- Handle error cases and retry logic

***Note:*** **This is purposely left open for you to think through. Coming up with good example to showcase the integration and power of Steel is a key skill we all will constantly need to be exercising to win over developers. Below is an implementation of the type of example we had in mind.**

<aside>
💡

### Hypothetical implementation: OpenTable Query Agent (Just an example, don’t do this)

Making a guide & cookbook example that builds custom tools to helps you find restaurant bookings on OpenTable. Wraps the document loader into custom tools. Using these two tools and an agent framework, users can ask about restaurant availabilities and get more details about potential options.

1. **Reservation Search Tool**
    - Input: location, date, time, party size
    - Output: available restaurant options with time slots
    - Handle pagination and filtering
    - Error handling for no results
2. **Get Restaurant Data Tool**
    - Input: restaurant url
    - Output: more comprehensive data about a specific restaurant along with images that could be fed into the agent.
</aside>

## 3. Documentation Requirements

We follow the [Diátaxis framework](https://diataxis.fr/) for documentation. For this project, create a **Tutorial**:
- Step-by-step guide implementing the Steel + Langchain integration to build the example above
- Clear code samples and explanations
- Testing instructions

In addition the repo's README is a key opportunity to provide value to users, we're looking for:
- Clear installation instructions
- Quick start guide
- Architecture overview
- Usage examples
- Demo video/gif embedded

## 4. Demonstration Requirements

- Demo video/gif
    - How do you help people visualize the example? You can imagine we announce the integration by showcasing a video/gif of the example we built using it from the cookbook.
    - It doesn’t need to be long or complicated, just needs to be clear and, ideally, impressive.
    - I would suggest you work backwards from this into the example that you build for the cookbook
    - Can just be a terminal-based demo leveraging the live viewer (don’t need to build a UI to visualize it)

## Success Criteria

1. Technical
    - Working Steel loader in Langchain
    - Functional restaurant booking example
    - Clean, well-organized code
    - Proper error handling
    - Thoughtful and well rounded tests
2. Documentation
    - Clear, complete tutorial
    - Well-structured how-to guide
    - Professional README
    - Inline code documentation
3. Demo
    - Clear, concise video demonstration
    - Shows full functionality
    - Highlights key features
4. How you work
    - Collaborative
    - Seek feedback early and often
    - High code and documentation quality standards

## Team

We’re here to be a resource. Our discord group chat is the best way to communicate with all of us and keep us updated on your progress. Feel free to request to hop on a call, pair program through anything, or generally just ping for anything.

### **How We Work**

Some projects at Steel work fairly independently. We like to stay relatively focused and heads down. Don’t mistake our quiet work environment for lack of interest in collaborating. 

Our communication style is not typically focused on immediate reassurance. We trust you to be confident and proactive in your decisions. Don't worry if you don't hear much in the way of positive feedback from us. Keep us updated as needed, and feel free to request immediate feedback if your next steps are dependent on it.

## Schedule

The timeline for this project is 5 days. We made that a stretch goal and we don’t expect you to finish the entire project by the end of it. At the end of the 5 days, we’ll hop on a call and you can take Nasr and Hussien through your work. Format is up to you. At the end of the presentation, we’ll have a dialogue about the project and if you have any other thoughts to share about the product or ways you could expand beyond your project, that's always great to hear too.


---
