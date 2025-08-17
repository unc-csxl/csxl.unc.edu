/**
 * Calendar Event is a standardized model for any events
 * that will be displayed in the calendar view
 *
 * @author David Foss
 * @copyright 2025
 * @license MIT
 */

import { TimeRange } from './time-range';

export interface CalendarEvent extends TimeRange {
  id: number;
}
