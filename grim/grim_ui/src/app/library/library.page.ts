import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { MagicService } from '../services/magic.service'
import { UtilityService } from '../services/utility.service'
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-library',
  templateUrl: './library.page.html',
  styleUrls: ['./library.page.scss'],
})
export class LibraryPage implements OnInit {

  public api_url = environment.api_url
  public grims: any;
  public streamlit_url = environment.streamlit_url
  public searchTerm = ""

  constructor(public magicService: MagicService, public navCtrl: NavController, public utilityService: UtilityService, private http: HttpClient) { }

  ngOnInit() {
    this.getGrims()
  }

  //TODO
  downloadGrim(grim) {
    console.log(grim)
  }

  ionViewDidEnter() {
    this.getGrims()
  }

  checkSearch(grim) {

    if (this.searchTerm == "") {
      return true
    }
    //if spell name contains string return true
    if (grim["name"].toLowerCase().includes(this.searchTerm.toLowerCase())) {
      return true
    } else {
      return false
    }
  }

  viewGrim(grim) {
    this.magicService.isBlank = false
    this.magicService["Data"]["curr_grim"] = grim
    this.utilityService.navURL("/grim-view")

  }

  castGrim(grim) {
    console.log("Going to cast grim " + grim["name"])


    //Send post request with spells to backend
    // POST formData to Server
    let headers = new HttpHeaders({
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    });

    var url = this.api_url + "/launch_grim"
    console.log("calling this url: " + url);

    this.http.post(url, grim, { headers: headers }).toPromise()
      .then((data) => { // Success
        console.log(data)
        //open new url
        window.open(this.streamlit_url, '_blank');
      }, (err) => {
        console.log("ok we should back out");
        console.log(err);
      })
  }

  getGrims() {
    console.log("getting grims")

    let headers = new HttpHeaders({
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    });
    var url = this.api_url + "/get_grims"
    this.http.get(url, { headers: headers }).toPromise()
      .then((data) => { // Success

        this.grims = data["grims"]
        console.log(this.grims)

      }, (err) => {
        console.log("ok we should back out");
        console.log(err);
        this.utilityService.presentModelAlert("Error try again")
      })



  }
}
