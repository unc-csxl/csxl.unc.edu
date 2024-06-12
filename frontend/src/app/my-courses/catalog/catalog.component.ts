import { Component } from '@angular/core';

@Component({
  selector: 'app-catalog',
  templateUrl: './catalog.component.html',
  styleUrls: ['./catalog.component.css']
})
export class CatalogComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'catalog',
    title: 'Catalog',
    component: CatalogComponent
  };

  /** Links for the tab bar */
  public links = [
    { label: 'Users', path: '/academics/catalog' },
    { label: 'Roles', path: '/academics/offerings' }
  ];
}
