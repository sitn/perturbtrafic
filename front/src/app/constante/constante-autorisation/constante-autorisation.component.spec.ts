import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConstanteAutorisationComponent } from './constante-autorisation.component';

describe('ConstanteAutorisationComponent', () => {
  let component: ConstanteAutorisationComponent;
  let fixture: ComponentFixture<ConstanteAutorisationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConstanteAutorisationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConstanteAutorisationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
