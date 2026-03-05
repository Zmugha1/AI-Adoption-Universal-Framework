/**
 * Format a Date to ISO 8601 string.
 * @throws Error if date is invalid
 */
export function formatDate(date: Date): string {
  const time = date.getTime();
  if (Number.isNaN(time)) {
    throw new Error('Invalid date');
  }
  return date.toISOString();
}
