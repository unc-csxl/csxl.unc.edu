/**
 * TimeRange abstracts out start and end time fields for
 * time-sensitive models. TimeRange enables all time-
 * sentitive models to use the same structure for easy
 * comparisons between times / dates and managing converting
 * JSONified time data to TypeScript `Date` objects.
 *
 * @author Kris Jordan <kris@cs.unc.edu>
 */

export interface TimeRangeJSON {
  start: string;
  end: string;
}

export interface TimeRange {
  start: Date;
  end: Date;
}
