import { Component } from '@angular/core';
import { showcaseResolver } from './showcase.resolver';
import { ActivatedRoute } from '@angular/router';
import { ShowcaseProject } from './showcaseproject.model';

@Component({
  selector: 'app-showcase',
  templateUrl: './showcase.component.html',
  styleUrls: ['./showcase.component.css']
})
export class ShowcaseComponent {
  /** Route information */
  public static Route = {
    path: 'showcase',
    title: 'COMP 423 Showcase',
    component: ShowcaseComponent,
    canActivate: [],
    resolve: { projects: showcaseResolver }
  };

  projects: Map<String, ShowcaseProject[]> = new Map();

  public displayedColumns: string[] = ['Team', 'Members', 'Links'];

  constructor(private route: ActivatedRoute) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      projects: ShowcaseProject[];
    };

    data.projects.forEach((project) => {
      let list = this.projects.get(project.type) ?? [];
      list.push(project);
      this.projects.set(project.type, list);
    });

    console.log(this.projects);
  }

  convertListToText(names: string[]): string {
    let str = '';

    for (let name of names) {
      if (name != '') {
        str += name;
        str += ', ';
      }
    }

    return str.slice(0, -2);
  }
}
