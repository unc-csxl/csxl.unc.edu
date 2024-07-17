/**
 * The Applications Model defines the shape of applications
 * data from the backend.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

export interface ApplicationSectionChoice {
  id: number;
  subject_code: string;
  course_number: string;
  section_number: string;
}
