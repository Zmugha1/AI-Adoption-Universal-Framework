import { formatDate } from '../../src/utils/helpers';

describe('formatDate', () => {
  it('should format standard date to ISO string', () => {
    expect(formatDate(new Date('2026-03-04'))).toBe('2026-03-04T00:00:00.000Z');
  });

  it('should handle epoch date', () => {
    expect(formatDate(new Date(0))).toBe('1970-01-01T00:00:00.000Z');
  });

  it('should handle invalid date', () => {
    expect(() => formatDate(new Date('invalid'))).toThrow();
  });
});
