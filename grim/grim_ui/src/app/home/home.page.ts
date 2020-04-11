import { Component } from '@angular/core';
import { NavController } from '@ionic/angular';
import { MagicService } from '../services/magic.service'
import { UtilityService } from '../services/utility.service'
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {

  public api_url = environment.api_url

  constructor(public magicService: MagicService, public navCtrl: NavController,public utilityService: UtilityService) {}

}
