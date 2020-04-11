import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ConjurePage } from './conjure.page';

const routes: Routes = [
  {
    path: '',
    component: ConjurePage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ConjurePageRoutingModule {}
