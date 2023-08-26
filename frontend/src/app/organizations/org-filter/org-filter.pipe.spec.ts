import { OrganizationFilterPipe } from './org-filter.pipe';

describe('FilterPipe', () => {
  it('create an instance', () => {
    const pipe = new OrganizationFilterPipe();
    expect(pipe).toBeTruthy();
  });
});
