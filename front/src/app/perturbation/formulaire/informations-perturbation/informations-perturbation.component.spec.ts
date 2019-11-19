import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InformationsPerturbationComponent } from './informations-perturbation.component';

describe('InformationsPerturbationComponent', () => {
  let component: InformationsPerturbationComponent;
  let fixture: ComponentFixture<InformationsPerturbationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InformationsPerturbationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InformationsPerturbationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
