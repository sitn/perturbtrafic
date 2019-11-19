import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConstanteFermetureUrgenceComponent } from './constante-fermeture-urgence.component';

describe('ConstanteFermetureUrgenceComponent', () => {
  let component: ConstanteFermetureUrgenceComponent;
  let fixture: ComponentFixture<ConstanteFermetureUrgenceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConstanteFermetureUrgenceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConstanteFermetureUrgenceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
