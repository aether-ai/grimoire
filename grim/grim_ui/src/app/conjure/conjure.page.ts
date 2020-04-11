import { Component, OnInit } from '@angular/core';
import { MagicService } from '../services/magic.service'
import { UtilityService } from '../services/utility.service'
import { NavController } from '@ionic/angular';
import { AlertController, LoadingController } from '@ionic/angular';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { DomSanitizer } from "@angular/platform-browser";

@Component({
  selector: 'app-conjure',
  templateUrl: './conjure.page.html',
  styleUrls: ['./conjure.page.scss'],
})
export class ConjurePage implements OnInit {

  public api_url = environment.api_url
  public streamlit_url = environment.streamlit_url
  public spell_mode = "conjure"
  public conjure_type = "grim"
  public spells: any
  public new_grim = []
  public new_grim_name: String = ""
  public new_grim_desc: String = ""
  public spells_dict = {}
  public showTable = false
  public spells_map: any;
  public spell_view = "card"
  public searchTerm = ""
  public safeUrl: any


  dtOptions: DataTables.Settings = {};

  constructor(private http: HttpClient, public magicService: MagicService, public navCtrl: NavController, public utilityService: UtilityService, public alertController: AlertController, private sanitizer: DomSanitizer) { 

    this.sanitizer = sanitizer;


  }

  checkSearch(spell) {

    if (this.searchTerm == "") {
      return true
    }

    //if spell name contains string return true
    if (spell["spell_name"].toLowerCase().includes(this.searchTerm.toLowerCase())) {
      return true
    } else {
      return false
    }
  }

  ionViewDidEnter() {
    this.resetGrim()
  }

  ngOnInit() {
    this.dtOptions = {
      pageLength: 10
    };
    this.safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(environment.streamlit_url);
    this.getSpells()
    this.resetGrim()
  }

  ifRealGrim() {

    if (this.new_grim.length < 1) {
      return false
    }

    if (this.new_grim_name.length < 1) {
      return false
    }

    if (this.new_grim_desc.length < 1) {
      return false
    }

    return true





  }

  segmentChanged(ev: any) {
    //console.log('Segment changed', ev);
    this.spell_view = ev["detail"]["value"]
    //console.log(this.spell_view)
  }

  inNewGrim(spell) {
    var spell_key = spell["spell_type"] + "_" + spell["spell_name"]
    var index = this.new_grim.indexOf(spell_key)

    if (index == -1) {
      return false
    } else {
      return true
    }

  }

  getSpells() {
    //console.log("getting spells")

    let headers = new HttpHeaders({
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    });

    var url = this.api_url + "/get_spells"



    this.http.get(url, { headers: headers }).toPromise()
      .then((data) => { // Success

        //console.log("got spells")

        this.spells = data["spells"]
        this.spells_map = data["spells_map"]
        //console.log(this.spells)
        //console.log(this.spells_map)

        //fill up spell_dict
        this.spells.forEach((spell) => {

          var spell_dict_key = spell["spell_type"] + "_" + spell["spell_name"]
          this.spells_dict[spell_dict_key] = spell

        });

        this.showTable = true


      }, (err) => {
        //console.log("ok we should back out");
        console.log(err);
        this.utilityService.presentModelAlert("Error try again")
      })



  }
  change_conjure_type(ctype) {
    this.conjure_type = ctype

  }

  resetGrim() {
    //console.log("getting spells")

    let headers = new HttpHeaders({
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    });

    var url = this.api_url + "/reset_grim"



    this.http.get(url, { headers: headers }).toPromise()
      .then((data) => { // Success

        console.log("reset grim")

      }, (err) => {
        console.log("problem trying to reset");
        console.log(err);
        //this.utilityService.presentModelAlert("Error try again")
      })



  }

  removeFromGrim(spell) {
    var spell_key = spell["spell_type"] + "_" + spell["spell_name"]
    var index = this.new_grim.indexOf(spell_key)
    this.new_grim.splice(index, 1)
    this.testGrim()
  }

  metRequirements(spell) {

    //check len of reqs
    if (spell["reqs"].length == 0) {
      //console.log(" it is true")
      return true;
    }

    var flag = true

    //else check if all requirments have been added
    spell["reqs"].forEach((req) => {
     // console.log("this is a req")
      //console.log(req)
     // console.log(this.new_grim)


      var index = this.new_grim.indexOf(req)

      if (index == -1) {
        flag = false
      }

    });

    return flag

  }


  addToGrim(spell) {
    var spell_key = spell["spell_type"] + "_" + spell["spell_name"]
    this.new_grim.push(spell_key)
    //console.log(" about to test grim")
    this.testGrim()
    //console.log(" tested grim")
  }

  createGrim() {

    //console.log("Creating grim")

    //Send post request with spells to backend
    // POST formData to Server
    let headers = new HttpHeaders({
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    });

    var grim_spells = []

    this.new_grim.forEach((spell) => {
      grim_spells.push(this.spells_dict[spell])
    });


    var grim_data = {}
    grim_data["name"] = this.new_grim_name
    grim_data["value"] = this.new_grim_desc
    grim_data["spells"] = grim_spells

    var url = this.api_url + "/create_grim"
    //console.log("calling this url: " + url);

    //this.utilityService.presentLoading()

    this.http.post(url, grim_data, { headers: headers }).toPromise()
      .then((data) => { // Success
        //console.log(data)
        //this.utilityService.dismissLoading()

        //check if error
        if (data["error"]) {
          console.log("Graceful error")
          this.utilityService.presentModelAlert(data["error"])
          return
        }


        this.utilityService.presentModal("Grimoire created", "Complete")
        // this.showResults = true
        // this.results = data

        //refresh grims
        //this.get_grims()

      }, (err) => {
        //this.utilityService.dismissLoading()
        //console.log("ok we should back out");
        console.log(err);
      })



  }



  testGrim() {
    //console.log("testing grim")
    //Send post request with spells to backend
    // POST formData to Server
    let headers = new HttpHeaders({
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    });

    var grim_spells = []

    this.new_grim.forEach((spell) => {
      grim_spells.push(this.spells_dict[spell])
    });

    var grim_data = {}
    grim_data["spells"] = grim_spells

    var url = this.api_url + "/test_grim"
    console.log("calling this url: " + url);
    //this.utilityService.presentLoading()
    this.http.post(url, grim_data, { headers: headers }).toPromise()
      .then((data) => { // Success
        console.log(data)
        //this.utilityService.dismissLoading()
        //this.utilityService.presentModal("Grimoire created","Complete")
        // this.showResults = true
        // this.results = data
      }, (err) => {
        //this.utilityService.dismissLoading()
        console.log("ok we should back out");
        console.log(err);
      })
  }

}
