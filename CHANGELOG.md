## [1.1.0] - 2025-08-09

### Fixed

*   **Issue 1:** Corrected inconsistent styling on the `/admin/clinics` page by applying Tailwind CSS to match the rest of the admin section.
*   **Issue 2:** Fixed an "Internal Server Error" on the `/admin/master-data` page by ensuring that all master data tables are correctly populated for all clinics.
*   **Issue 3:** Resolved an issue where "Bloque Horario de Alta" and "criterios de ajuste de estancia" were missing data when creating a new ticket.
*   **Issue 4:** Implemented disaggregated name fields in the ticket list view, allowing users to see and select "Primer Nombre", "Segundo Nombre", "Apellido Paterno", and "Apellido Materno" as separate columns.
*   **Issue 5:** Fixed the column sorting functionality in the ticket list view.