import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { GrimViewPage } from './grim-view.page';

describe('GrimViewPage', () => {
  let component: GrimViewPage;
  let fixture: ComponentFixture<GrimViewPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GrimViewPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(GrimViewPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
