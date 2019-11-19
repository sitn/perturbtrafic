import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RemarquePerturbationComponent } from './remarque-perturbation.component';

describe('RemarquePerturbationComponent', () => {
  let component: RemarquePerturbationComponent;
  let fixture: ComponentFixture<RemarquePerturbationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RemarquePerturbationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RemarquePerturbationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
