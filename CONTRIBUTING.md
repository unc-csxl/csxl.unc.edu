# Contributing Guidelines

This document outlines the guidelines and expectations for the contributing process into the XL repository!

## Review Process for Large Features

Large features should undergo three major review cycles: 

### **Step 1. Design Review**

The first review should be a complete design review. For large features, *both* backend and frontend design should be reviewed and approved before coding actually begins. This makes the entire backend review process significantly easier, as major schema or system design overhauls would have been discussed before developers spent time coding solutions. The design review can be in the form of a Markdown *design document* (or equivalent). This design document will include the following:
- [ ] Clear use case / problem statement / "user stories" of the problem are defined.
- [ ] Entity diagrams, with relationships and field types specified, are defined.
- [ ] The implementation of service methods, as well as the general idea for APIs, should be discussed. 
- [ ] Plan for frontend design is discussed. We encourage a complete design plan completed with the CSXL Figma template, although sketches are also permissible.

### **Step 2: Backend Design Review**

The second design review focuses on the backend implementation of the design specified in Part 1. The code submitted in a pull request for this review should usually just include progress on the backend - including substantial frontend functionality is fine, however the backend will solely be reviewed first! If there are major changes required to your backend, you will then need to propagate those changes forwards to the frontend. This process ensures that the reviewers are not overloaded with code and have the chance to more thoroughly review the backend code for production. Below is a checklist of items that your code in this step should include:
**Entities**
- [ ] Ensure that the `backend.script.create_database` and `backend.script.reset_demo` scripts still run as expected.
- [ ] Ensure that all entities are appropriately documented.
**Models and Services**
- [ ] All basic CRUD functionality has been provided.
- [ ] Integrate pagination where the length of the average expected output exceeds ~30.
- [ ] Permissions are enforced on service functions where necessary. ***Include any added permissions to your PR so that they can be added to the Wiki!***
- [ ] Service functions are documented with Python docstrings provided. Ideally, comments should be added throughout so that new developers can have a sense of what is going on. **Remember - COMP 423 students will be reading your code!**
- [ ] Unit tests have been written for every new service function, *and* test coverage for the feature is at (or close to) 100%. ***‼️ This is extremely important! Reviewers will not complete a backend review unless your PR makes a good effort at writing tests.***
- [ ] Models include just enough information for the frontend to function without exposing too much data.
**APIs**
- [ ] All APIs run as expected from the `/docs` URL.
- [ ] APIs are entirely documented with Python docstrings provided.
- [ ] Correct models are returned, and sensitive data is not accidentally exposed.

### **Step 3: Frontend Review**

The final design review focuses on the frontend implementation of your design specified in Part 1, connected to the backend you implemented in Part 2. This is often the final review completed before migrations are written and a merge into `main` can be performed. This review will focus on polishing UI/UX to Material 3 guidelines.

**Angular Frontend**
- [ ] The new frontend service should include all necessary endpoints for the feature.
- [ ] All service methods return observables where needed.
- [ ] Angular Signals are used to store reactive objects, where needed.
- [ ] Service is documented with TS docstrings.
- [ ] Models are placed in a `feature.model.ts` file.
- [ ] New components should be declared in a feature module.
- [ ] Component HTML utilizes the new `@` standard (instead of the directives `ngIf`, `ngFor`, etc).
- [ ] Material 3 elements are used thoughtfully throughout features, with attention to placement, responsive CSS (for mobile devices), and adherence to the M3 theme (color and typography system)!

## Expedited Review for Smaller Features

Smaller features and pull requests may implement small to medium-size changes to the existing codebase, and therefore, three separate reviews may not be necessary. However, all of the checklist items for Step 2 and Step 3 should be completed, and will be checked by the reviewers!
