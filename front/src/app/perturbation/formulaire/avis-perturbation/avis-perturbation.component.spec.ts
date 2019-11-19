import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AvisPerturbationComponent } from './avis-perturbation.component';

describe('AvisPerturbationComponent', () => {
  let component: AvisPerturbationComponent;
  let fixture: ComponentFixture<AvisPerturbationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AvisPerturbationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AvisPerturbationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
