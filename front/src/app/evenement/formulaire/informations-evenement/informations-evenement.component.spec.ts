import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InformationsEvenementComponent } from './informations-evenement.component';

describe('InformationsEvenementComponent', () => {
  let component: InformationsEvenementComponent;
  let fixture: ComponentFixture<InformationsEvenementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InformationsEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InformationsEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
