import { OrganizationFilterPipe } from './organization-filter.pipe';

describe('FilterPipe', () => {
  it('create an instance', () => {
    const pipe = new OrganizationFilterPipe();
    expect(pipe).toBeTruthy();
  });
});
