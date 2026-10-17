# Coworking Operating Hours Editor Plan

## Goal and scope

Add an **Operating Hours** tab immediately after **Room Reservations** in the ambassador view. Ambassadors can edit active hours and add, edit, or delete future hours. Reuse the app's widgets and Material conventions, specifically the date/time controls from the New Office Hours event editor.

This plan includes a new `PUT /api/coworking/operating_hours/{id}` endpoint and the service, persistence, permissions, error handling, and tests needed to enforce valid, nonconflicting hours. Existing GET, POST, and DELETE endpoints remain the other integration points. No new frontend routes are required.

The implementation follows this plan. Deployment and verification notes are recorded at the end of the document. No Alembic migration or schema change is included.

## Current implementation and reuse opportunities

| Area                 | Existing implementation                                                                                                                                                                                                     | Planned use                                                                             |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Ambassador shell     | [AmbassadorPageComponent](../frontend/src/app/coworking/ambassador-home/ambassador-home.component.ts)                                                                                                                       | Add the third tab and coordinate its local selection state.                             |
| Tabs                 | [TabContainerWidget](../frontend/src/app/shared/tab-container/tab-container.widget.ts)                                                                                                                                      | Add optional local content support while preserving existing routed consumers.          |
| List layout          | [Ambassador room reservations](../frontend/src/app/coworking/ambassador-home/ambassador-room/ambassador-room.component.html)                                                                                                | Reuse outlined cards, responsive Material tables, spacing, and date presentation.       |
| Date/time fields     | [Office Hours editor template](../frontend/src/app/my-courses/course/office-hours/office-hours-editor/office-hours-editor.component.html)                                                                                   | Extract the start/end field pair for both editors.                                      |
| Form validation      | [Office Hours editor component](../frontend/src/app/my-courses/course/office-hours/office-hours-editor/office-hours-editor.component.ts)                                                                                    | Extract reusable start/end validation while leaving recurrence rules with Office Hours. |
| Hours data           | [Coworking models](../frontend/src/app/coworking/coworking.models.ts)                                                                                                                                                       | Reuse `OperatingHours`, `OperatingHoursJSON`, and parsing conventions.                  |
| Public hours display | [Operating hours panel](../frontend/src/app/shared/operating-hours-panel/operating-hours-panel.widget.ts) and [hours dialog](../frontend/src/app/coworking/widgets/operating-hours-dialog/operating-hours-dialog.widget.ts) | Preserve the public display and refresh its underlying coworking status after changes.  |
| Backend              | [Hours API](../backend/api/coworking/operating_hours.py), [service](../backend/services/coworking/operating_hours.py), and [entity](../backend/entities/coworking/operating_hours_entity.py)                                | Add update support and consistent invariant enforcement.                                |

The Office Hours start/end controls are currently inline template markup, not standalone widgets. They use `matInput` with `type="datetime-local"`, outlined `mat-form-field` containers, reactive form controls, and `yyyy-MM-ddTHH:mm` formatting. The coworking reservation `DateSelector` is coupled to reservation state and is not the reuse target.

## User experience

### Tab and layout

The tab order is **XL Reservations → Room Reservations → Operating Hours**. Use a schedule icon consistent with the existing icon-and-label tabs.

| Section      | Membership           | Actions                                              |
| ------------ | -------------------- | ---------------------------------------------------- |
| Active Hours | `start <= now < end` | Edit only; no Delete control.                        |
| Future Hours | `start > now`        | Add Hours at section level; Edit and Delete per row. |
| Past hours   | `end <= now`         | Excluded from this editor's lists.                   |

Show the Active Hours card only when an active interval exists. Otherwise show a concise closed status. Always show the Future Hours card, including an empty message and Add Hours when no future intervals are loaded.

Use Date, Start, End, and Actions columns, ordered by start time. Reuse one hours-list widget for the two sections, with explicit allowed actions. Show both dates when an interval crosses midnight. Apply the current theme, typography, spacing, and responsive table conventions.

Load from the start of today in Eastern Time through the next 30 days initially, so completed hours today are available when choosing the new-entry default. Show the loaded range and a **Load more** action that extends the end by 30 days. Do not silently treat the API's default one-week result as the complete future schedule. Deduplicate results by ID, retain the loaded horizon when refreshing, and include any active interval that began before the query start.

### Add and edit

Use one Material dialog for both operations, titled **Add Operating Hours** or **Edit Operating Hours**. Provide Start Time and End Time fields using the shared Office Hours controls, plus Cancel and Save.

- New hours default to 10:00 AM–6:00 PM Eastern today when no hours overlap today, even when 10:00 AM has passed; otherwise default to tomorrow. Both fields remain editable.
- Editing prepopulates a copy of the selected interval. Cancel leaves stored values unchanged.
- Require complete, valid dates and `end > start`. Show the same style of range error as the Office Hours editor.
- Add Hours allows today or a future date, including a start time earlier today. Active edits also accept the interval's existing past start.
- Both start and end remain editable. Do not introduce an unrequested end-time-only restriction for active hours.
- Validate against loaded hours for immediate feedback, excluding the edited ID. Treat the backend as authoritative because other hours may be outside the loaded range or changed by another ambassador.
- Disable Save while invalid or submitting. Preserve inputs and show an actionable error when saving fails; close only after success.
- Present the facility timezone clearly and use a consistent conversion between form values, API values, and displayed hours.

### Delete and feedback

Use a Material confirmation dialog naming the future interval, with Cancel and Delete actions. Recheck that the interval is still future before submitting. The backend also checks this rule using current stored values.

Keep rows visible until a mutation succeeds. Show a snackbar on success, refresh the schedule and coworking status, and show a recoverable error on failure. If a record has disappeared, explain that it is no longer available and refresh the list.

Differentiate loading, empty, and failed-load states. Provide Retry for failures. When time passes, move future intervals into Active Hours and remove expired intervals without requiring a page reload. Refresh on tab activation and window focus, and maintain a lifecycle-safe timer while the panel is visible. Do not overwrite an open form during background refresh.

### Accessibility and Material conventions

Use actual Material tab controls and their keyboard behavior, visible field labels, associated error messages, descriptive action names, and clear focus indicators. Keep the start/end fields side by side when space permits and stack them on smaller screens. Dialogs retain Escape behavior, focus trapping, and focus restoration; after deleting a row, return focus to a sensible remaining action.

These choices follow the [Angular Material tabs](https://github.com/angular/components/blob/main/src/material/tabs/tabs.md) and [dialog](https://github.com/angular/components/blob/main/src/material/dialog/dialog.md) guidance.

## Frontend implementation

### Preserve the existing routes

Extend `TabContainerWidget` with opt-in local panel content and selected-state support. Preserve its existing route-link behavior by default. Operating Hours selects local content in the ambassador shell without navigating to a new URL.

Keep the existing `/coworking/ambassador/xl` and `/coworking/ambassador/room` routes and guards. Clear the local selection when a reservation tab is clicked, including when its URL is already active. Synchronize selection on router navigation so direct links and browser Back/Forward still work. Limit the shell's current default redirect to visits without a selected child route so it does not override direct Room Reservations links.

Enforce ambassador visibility and hours-action permissions for the local panel explicitly; it cannot rely on a new child route guard. Regression-check other consumers of the shared tab container.

### Extract the Office Hours field pair

Create a small shared date/time range widget under `frontend/src/app/shared/`. Accept start/end form controls and configurable labels, keeping ownership of the form with each editor. Preserve the Office Hours field appearance, local datetime format, required state, and parent form reset behavior.

Extract the start-before-end validator into a shared helper that accepts control names. Leave the Office Hours recurrence-end validation and course-specific behavior in that feature. Replace only the existing start/end markup and corresponding range validation in Office Hours; do not import the whole course editor into coworking.

Keep temporal rules such as today-or-later creation in the coworking form. Do not copy the Office Hours recurrence-date adjustment into the shared widget. Test timezone serialization separately from presentation and avoid applying timezone conversion twice. If an hours-specific adapter is needed for the backend's timezone-naive Eastern-time values, keep it scoped to coworking rather than changing every use of `TimeRange`.

### Add hours components and service

Add an ambassador hours panel, a reusable hours-list widget, and an add/edit dialog. Use a small confirmation dialog or template for deletion. Register them in the appropriate owning module and import the Material and reactive-form modules they actually use. The current ambassador components are declared in `CoworkingModule`, despite the separate ambassador routing module; follow actual declaration ownership and avoid duplicate declarations.

Add an `OperatingHoursService` on the frontend with list, create, update, and delete operations. Use existing model parsers where their timezone behavior matches the verified API contract. Keep HTTP behavior out of the list widget. Track pending state per operation, handle permission and validation failures, and refresh `CoworkingService.pollStatus()` after successful writes.

## Backend contract

| Method and path                              | Request                                          | Successful response                                             |
| -------------------------------------------- | ------------------------------------------------ | --------------------------------------------------------------- |
| `GET /api/coworking/operating_hours`         | Explicit `start` and `end` query parameters      | Existing list of `OperatingHours`.                              |
| `POST /api/coworking/operating_hours`        | Existing `TimeRange` body                        | Existing newly created `OperatingHours`.                        |
| `PUT /api/coworking/operating_hours/{id}`    | Complete `TimeRange` body with `start` and `end` | `200` with the updated `OperatingHours`, including the same ID. |
| `DELETE /api/coworking/operating_hours/{id}` | Existing path ID                                 | Preserve the existing success contract.                         |

PUT replaces both time fields on the existing record. The path ID identifies the record; a body ID is unnecessary. A valid unchanged update succeeds without treating the record as conflicting with itself. Missing records return 404 rather than creating a replacement.

Use `registered_user` authentication and enforce `coworking.operating_hours.update` on `coworking/operating_hours/{id}` in the service. Keep create and delete action names consistent with their current definitions.

Use the application's existing `{"message": "..."}` convention for domain errors. Preserve authentication behavior and the existing 403/404 handlers. Return 422 for invalid time input and 409 for conflicting operating hours or an attempted deletion of hours that are no longer future. Map the existing `OperatingHoursCannotOverlapException` for both POST and PUT; it currently has no dedicated handler.

## Backend invariants and persistence

### Valid times and overlap policy

Reuse `TimeRange` validation so start/end are valid datetimes, normalized consistently, and `end > start`. Any required validation correction must retain existing consumers' behavior and have focused model tests. Avoid host-timezone-dependent comparisons: compare stored facility-local timestamps with a consistently derived America/New_York current time.

Preserve the existing operating-hours conflict policy. Another row conflicts when:

```text
other.start <= proposed.end AND other.end >= proposed.start
```

This policy rejects touching endpoints as well as partial overlaps, containment, and duplicate intervals. For example, 9:00–12:00 and 12:00–15:00 conflict under current behavior. Use the same policy for create, update, UI feedback, and persistence. Do not substitute the shared `TimeRange.overlaps()` helper without accounting for its different endpoint semantics.

Factor conflict lookup into a helper with an optional excluded ID. On update, exclude only the target record; query all other stored hours, including records outside the frontend's loaded window. Keep the public schedule query's ordering and range behavior intact.

Add `OperatingHoursService.update(subject, id, time_range)` with this sequence:

1. Enforce update permission and load the current entity, or raise not found.
2. Validate the proposed normalized range and check other records for conflicts.
3. Assign start/end to the existing entity and commit atomically.
4. Return the updated model with its original ID.

On failure, roll back and preserve the previous record. Editing must never be implemented as delete followed by create.

The editor creates today's or future intervals, but existing POST callers should not acquire unrelated new restrictions as a side effect of implementing PUT. Active edits remain supported. For DELETE, enforce `stored.start > now` in the service, using a fresh, locked record so a concurrent edit cannot bypass the check. Active and past intervals cannot be deleted through this workflow.

### Protect against concurrent writes

A service-level read-then-write conflict check alone can allow concurrent requests to write overlapping hours. Serialize all create, update, and delete operations with a PostgreSQL `SHARE ROW EXCLUSIVE` lock on the existing operating-hours table, acquired before the conflict query and held through commit or rollback. This lock permits ordinary readers while ensuring a waiting writer checks the schedule after the preceding writer commits. It also works when the table is empty, unlike locking only matching rows. [PostgreSQL table locks](https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-TABLES)

Enforce ordered times through the model and service, and apply the same overlap predicate to every service write. Keep transactions short and release locks on failures. Test competing writers using separate database sessions, including create/create, create/update, and update/update. These are application-write guarantees; direct SQL writes outside the service must observe the same validation rules.

No Alembic migration, new constraint, or schema change is part of this work.

### Permissions and reservation effects

Ensure the ambassador role has create, update, and delete permissions scoped to coworking operating hours. The current test/demo ambassador permissions include reservations but do not include these hours actions. Update fixtures and prepare an idempotent provisioning step for existing deployments; changing fixture data alone does not grant production access. Do not grant unrelated administrative capabilities.

Use existing `PermissionService` checks in the frontend as well as authoritative service enforcement. Verify with an ambassador account, not only a root account.

Changes to operating hours affect availability and open/closed status. Refresh those views after mutations and regression-test reservation queries against changed hours. Preserve existing reservations; this feature does not automatically cancel or resize them. Record the observed behavior when hours are shortened around existing reservations so the implementation does not introduce an implicit reservation policy change.

## Implementation sequence

1. **Backend rules and tests:** factor conflict validation, add update service behavior, cover self-exclusion and failed-update preservation, and enforce future-only deletion.
2. **Concurrency and permissions:** serialize schedule mutations within their transactions, test concurrent writers, and prepare ambassador permission provisioning.
3. **API:** add PUT, map domain errors consistently for create/update/delete, and test request/response and authorization behavior.
4. **Shared controls:** extract the Office Hours date/time fields and range validator, and verify the existing editor still behaves correctly.
5. **Ambassador integration:** add the in-place tab, list sections, frontend service, add/edit dialog, and delete confirmation.
6. **Verification:** exercise end-to-end ambassador flows, temporal boundaries, accessibility, responsive behavior, and reservation regressions.

Keep the changes focused on operating hours and the small shared pieces needed by the two editors. Recurring coworking schedules, bulk operations, historical management, new frontend routes, and a general calendar redesign are outside this plan.

## Validation and acceptance criteria

### Backend

- Update an active interval and a future interval successfully; retain the original ID.
- Accept an unchanged update and changes that overlap only the record's own original interval.
- Reject partial overlaps, full containment in either direction, duplicate ranges, and touching endpoints with another record.
- Reject missing or malformed datetimes, equal start/end, and end before start; verify offset normalization and DST-related round trips.
- Return 404 for missing IDs and 403 for insufficient permissions, with no mutation on failures.
- Reject deletion of active or past hours, including a future interval becoming active before the deletion is processed.
- Verify concurrent create/create, create/update, and update/update conflicts using separate database sessions. At most one conflicting write succeeds; the other yields a handled conflict.
- Verify the service revalidates supplied times and that transaction rollback leaves the session usable.
- Verify concurrent writes are safe without any schema changes.
- Regression-test existing create/delete/schedule behavior and reservation availability after hours change.

Extend [operating-hours service tests](../backend/test/services/coworking/operating_hours_test.py) and [time-range model tests](../backend/test/models/coworking/time_range_test.py) as needed. Add focused API tests using FastAPI's test client and dependency overrides. Use a controlled clock for exact start/end boundary tests instead of timing-dependent sleeps.

### Frontend and integration

- Verify tab order, existing direct links, repeated selection, Back/Forward, and unchanged behavior for other tab-container consumers.
- Verify active hours expose Edit only and future hours expose Add/Edit/Delete.
- Verify closed, loading, empty, failed-load, and retry states; load later hours beyond the initial date range.
- Verify add/edit/cancel/delete, validation failures, server conflicts, permission failures, and duplicate-click prevention.
- Verify future-to-active and active-to-past transitions, including while a delete confirmation is open.
- Verify the Office Hours editor's create/edit/reset and recurrence validation after shared-control extraction.
- Verify keyboard navigation, dialog focus, screen-reader labels, mobile layout, overnight intervals, and timezone round trips.
- Verify successful mutations refresh the schedule and public coworking status without changing existing reservations.

Use the repository's existing Playwright flow runner for browser verification where useful. The frontend has no configured unit-test target, so do not claim an `ng test` check exists or add a new test framework merely for this feature.

Run the relevant checks during implementation:

```bash
# From the repository root
uv run --project backend pytest backend/test/services/coworking/operating_hours_test.py backend/test/models/coworking/time_range_test.py
uv run --project backend pytest backend/test/services/coworking
uv run --project backend ruff format --check backend

# From frontend/
pnpm lint
pnpm exec ng build --configuration production --output-path /tmp/csxl-hours-editor-build
```

Include the newly added API and database-concurrency tests in the relevant test run. Run the full backend suite before merging because the shared time model and permission fixtures can affect other features.

The feature is complete when an authorized ambassador can manage the required active and future hours in the existing view, both editors share the intended date/time controls, invalid or conflicting writes are rejected even under concurrency, and the existing reservation and Office Hours workflows pass regression checks.

## Deployment and verification notes

No migration or schema change is required. Schedule writes use validation and a transaction-scoped lock on the existing operating-hours table. Existing installations need the three scoped ambassador permissions; the idempotent [permission grant script](../backend/script/deployments/operating_hours_permissions.py) adds missing permissions to the existing role:

```bash
uv run --project backend python -m backend.script.deployments.operating_hours_permissions
```

The permission grant was exercised against local development data. It does not alter the schema. Production deployment has not been performed.

Verification completed:

- The full backend suite passes: **615 tests**, using the project's Python 3.15 runtime.
- Changed Python files pass Pyright with the repository's Pylance diagnostic overrides. Ruff organizes their imports and checks backend formatting. A pre-existing invalid, unreachable WebSocket mount was removed after verifying that the earlier static mount matches the same paths; the separately registered WebSocket echo route and API docs still pass smoke checks.
- Backend service/API tests cover ordered times, self-exclusion, inclusive overlap boundaries, permissions, missing records, active/past deletion restrictions, concurrent writers, and idempotent permission grants.
- A reservation regression confirms that shortening hours updates availability while preserving an existing booking's times and state.
- Frontend lint and the production build pass. The build reports an initial-bundle budget warning of approximately 1.23 kB over the existing 1.57 MB budget.
- Browser checks with an ambassador account cover create, edit with the same ID, delete/cancel, active-only editing, server conflicts outside the loaded range, and preserved form values after failure.
- Controlled browser checks cover failed-load/retry and empty states, today's 10 AM default after 10 AM, tomorrow's default when completed hours exist today, future-to-active-to-past transitions, extended date ranges, and keyboard tab navigation.
- Eastern-time defaults and round trips were checked in a Los Angeles browser. The date helper was also checked with UTC and Los Angeles process timezones, including winter and summer dates.
- The existing Office Hours new-event editor retains range validation, recurrence validation, and Reset behavior; the existing-event editor loads both shared controls.
- Desktop and 390-pixel mobile captures were reviewed. Tables use the app's horizontal scrolling convention on narrow screens; dialog fields stack vertically. Temporary records used for browser testing were removed.

Screenshots: [desktop schedule](images/coworking-operating-hours/desktop.png), [edit dialog](images/coworking-operating-hours/edit-dialog.png), [mobile schedule](images/coworking-operating-hours/mobile.png), and [mobile dialog](images/coworking-operating-hours/mobile-dialog.png).
