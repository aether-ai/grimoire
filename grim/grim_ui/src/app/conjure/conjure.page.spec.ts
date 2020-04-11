import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { ConjurePage } from './conjure.page';

describe('ConjurePage', () => {
  let component: ConjurePage;
  let fixture: ComponentFixture<ConjurePage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConjurePage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(ConjurePage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
