import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConstanteComponent } from './constante.component';

describe('ConstanteComponent', () => {
  let component: ConstanteComponent;
  let fixture: ComponentFixture<ConstanteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConstanteComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConstanteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
