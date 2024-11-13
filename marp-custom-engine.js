const { Marp } = require('@marp-team/marp-core');

// Define your variables here
const variables = {
    BOOTCAMP_WEBSITE: "https://gem5bootcamp.gem5.org/",
    BOOTCAMP_ARCHIVE: "https://gem5bootcamp.github.io/2024",
    GITHUB_REPO: "https://github.com/gem5bootcamp/2024",
    GITHUB_CLASSROOM: "https://classroom.github.com/a/gCcXlgBs",
    GEM5_CODE: "https://github.com/gem5/gem5",
    GEM5_WEBSITE: "https://www.gem5.org/",
    GEM5_YOUTUBE: "https://youtube.com/@gem5",
    GEM5_SLACK: "https://gem5-workspace.slack.com/join/shared_invite/zt-2e2nfln38-xsIkN1aRmofRlAHOIkZaEA"
};

// Function to replace placeholders with actual values in the markdown content
function replaceVariables(content) {
    let updatedContent = content.toString();  // Ensure content is a string
    for (const [key, value] of Object.entries(variables)) {
        const placeholder = `{{${key}}}`;
        const regex = new RegExp(placeholder, 'g');
        updatedContent = updatedContent.replace(regex, value);
    }
    return updatedContent;
}

// Custom Marp engine class
class CustomMarpEngine extends Marp {
    // Override the render method to preprocess Markdown content
    render(markdown, options = {}) {
        const processedMarkdown = replaceVariables(markdown);  // Replace placeholders
        return super.render(processedMarkdown, options);       // Call Marp's render method
    }
}

module.exports = CustomMarpEngine;
