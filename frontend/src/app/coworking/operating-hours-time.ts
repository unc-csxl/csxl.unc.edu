/** Operating-hours forms use facility wall time, regardless of browser timezone. */
export const OPERATING_HOURS_TIMEZONE = 'America/New_York';

const inputFormatter = new Intl.DateTimeFormat('en-US', {
  timeZone: OPERATING_HOURS_TIMEZONE,
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
  hourCycle: 'h23'
});

export function operatingHoursInput(date: Date): string {
  const parts = Object.fromEntries(
    inputFormatter.formatToParts(date).map((part) => [part.type, part.value])
  );
  return `${parts['year']}-${parts['month']}-${parts['day']}T${parts['hour']}:${parts['minute']}`;
}

/** Default to today unless the schedule already contains hours on that Eastern date. */
export function newOperatingHoursRange(
  schedule: { start: Date; end: Date }[],
  now = new Date()
): { start: string; end: string } {
  const localNow = operatingHoursInput(now);
  const day = new Date(`${localNow.slice(0, 10)}T00:00:00Z`);
  const today = localNow.slice(0, 10);
  const nextDay = new Date(day);
  nextDay.setUTCDate(nextDay.getUTCDate() + 1);
  const tomorrow = nextDay.toISOString().slice(0, 10);
  const hasHoursToday = schedule.some(
    (hours) =>
      operatingHoursInput(hours.start) < `${tomorrow}T00:00` &&
      operatingHoursInput(hours.end) > `${today}T00:00`
  );
  if (hasHoursToday) day.setUTCDate(day.getUTCDate() + 1);
  const date = day.toISOString().slice(0, 10);
  return { start: `${date}T10:00`, end: `${date}T18:00` };
}

export function operatingHoursDate(date: Date): string {
  return date.toLocaleDateString('en-US', {
    timeZone: OPERATING_HOURS_TIMEZONE,
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
}

export function operatingHoursTime(date: Date): string {
  return date.toLocaleTimeString('en-US', {
    timeZone: OPERATING_HOURS_TIMEZONE,
    hour: 'numeric',
    minute: '2-digit'
  });
}
