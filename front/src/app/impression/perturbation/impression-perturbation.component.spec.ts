import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ImpressionPerturbationComponent } from './impression-perturbation.component';

describe('ImpressionPerturbationComponent', () => {
  let component: ImpressionPerturbationComponent;
  let fixture: ComponentFixture<ImpressionPerturbationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ImpressionPerturbationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ImpressionPerturbationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
