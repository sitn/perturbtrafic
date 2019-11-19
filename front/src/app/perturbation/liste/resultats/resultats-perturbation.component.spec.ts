import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ResultatsPerturbationComponent } from './resultats-perturbation.component';

describe('ResultatsPerturbationComponent', () => {
  let component: ResultatsPerturbationComponent;
  let fixture: ComponentFixture<ResultatsPerturbationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ResultatsPerturbationComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ResultatsPerturbationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
