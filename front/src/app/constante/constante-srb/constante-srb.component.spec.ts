import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConstanteSrbComponent } from './constante-srb.component';

describe('ConstanteSrbComponent', () => {
  let component: ConstanteSrbComponent;
  let fixture: ComponentFixture<ConstanteSrbComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConstanteSrbComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConstanteSrbComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
