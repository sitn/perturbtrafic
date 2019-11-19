import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GuichetCartoComponent } from './guichet-carto.component';

describe('GuichetCartoComponent', () => {
  let component: GuichetCartoComponent;
  let fixture: ComponentFixture<GuichetCartoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GuichetCartoComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GuichetCartoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
