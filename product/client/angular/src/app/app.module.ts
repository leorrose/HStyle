import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { FooterComponent } from './footer/footer.component';
import { HistoricalStyleGeneratorComponent } from './historical-style-generator/historical-style-generator.component';
import { AboutComponent } from './about/about.component';
import { TeamMemberCardComponent } from './team-member-card/team-member-card.component';
import { TeamMembersComponent } from './team-members/team-members.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@NgModule({
  declarations: [
    AppComponent,
    NavBarComponent,
    FooterComponent,
    HistoricalStyleGeneratorComponent,
    AboutComponent,
    TeamMemberCardComponent,
    TeamMembersComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
