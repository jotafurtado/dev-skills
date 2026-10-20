# Incident: stale selection and repeated refetches

Synthetic observations from an Agent-Native app. Installed source and exact
package versions have not been supplied. Causes must be treated as hypotheses.

- The app contains `app/hooks/use-navigation-state.ts`, but a new page attempts
  to import `useNavigationState` from Core instead of using the app hook.
- After navigating from project A to project B, the agent still receives A's
  selected record ID.
- The view-screen action loads any supplied record ID without checking the actor.
- A UI mutation updates the database, but a raw query with a custom cache key
  keeps displaying its old result.
- Agent edits appear after a full page reload.
- A newly added timer refetches every query each second, even on settings pages.
- Each component creates its own tab ID and polls navigation commands. Some
  navigate commands run twice, and writing selection causes visible jitter.
- A shared project list must show edits from a second user. Static settings
  pages have no comparable remote-update requirement.

Give an ordered investigation and repair plan that distinguishes UI actions,
local agent-run refreshes, and remote updates. No tests have been run.
