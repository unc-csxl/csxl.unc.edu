/**
 * The My Courses models defines the shape of My Courses data
 * retrieved from the My Courses Service and the API.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

export interface SectionOverview {
  number: string;
  meeting_pattern: string;
}

export interface CourseOverview {
  id: string;
  subject_code: string;
  number: string;
  title: string;
  sections: SectionOverview[];
  role: string;
}

export interface TermOverview {
  id: string;
  name: string;
  start: Date;
  end: Date;
  courses: CourseOverview[];
}

export interface TermOverviewJson {
  id: string;
  name: string;
  start: string;
  end: string;
  courses: CourseOverview[];
}

/**
 * Function that converts an TermOverviewJson response model to a
 * TermOverview model.
 *
 * This function is needed because the API response will return certain
 * objects (such as `Date`s) as strings. We need to convert this to
 * TypeScript objects ourselves.
 */
export const parseTermOverviewJson = (
  responseModel: TermOverviewJson
): TermOverview => {
  return Object.assign({}, responseModel, {
    start: new Date(responseModel.start),
    end: new Date(responseModel.end)
  });
};

export const parseTermOverviewJsonList = (
  responseModels: TermOverviewJson[]
): TermOverview[] => {
  return responseModels.map(parseTermOverviewJson);
};
