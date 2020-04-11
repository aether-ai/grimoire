import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { GrimViewPageRoutingModule } from './grim-view-routing.module';

import { GrimViewPage } from './grim-view.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    GrimViewPageRoutingModule
  ],
  declarations: [GrimViewPage]
})
export class GrimViewPageModule {}
