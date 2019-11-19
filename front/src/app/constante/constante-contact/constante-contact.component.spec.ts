import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConstanteContactComponent } from './constante-contact.component';

describe('ConstanteContactComponent', () => {
  let component: ConstanteContactComponent;
  let fixture: ComponentFixture<ConstanteContactComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConstanteContactComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConstanteContactComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
