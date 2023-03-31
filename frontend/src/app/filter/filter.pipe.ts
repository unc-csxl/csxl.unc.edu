import { Pipe, PipeTransform } from '@angular/core';
import { Observable } from 'rxjs';
import { Organization } from '../organizations/organizations.service';
import { map } from 'rxjs/operators';

@Pipe({
  name: 'filter'
})
export class FilterPipe implements PipeTransform {

  transform(value: Observable<Organization[]>, input: String): any {
    if (input) {
      return value.pipe(map(value => value.filter(val => val.name.toLowerCase().startsWith(input.toLowerCase()))));
    } else {
      return value;
    }
  }

}
