import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { GrimViewPage } from './grim-view.page';

const routes: Routes = [
  {
    path: '',
    component: GrimViewPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class GrimViewPageRoutingModule {}
