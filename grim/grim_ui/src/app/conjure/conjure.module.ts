import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ConjurePageRoutingModule } from './conjure-routing.module';

import { ConjurePage } from './conjure.page';
import { DataTablesModule } from 'angular-datatables';


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    DataTablesModule,
    ConjurePageRoutingModule
  ],
  declarations: [ConjurePage]
})
export class ConjurePageModule {}
