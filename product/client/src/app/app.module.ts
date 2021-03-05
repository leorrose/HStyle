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
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { DemoComponent } from './demo/demo.component';
import { SingleImageUploaderComponent } from './single-image-uploader/single-image-uploader.component';
import { NgxDropzoneModule } from 'ngx-dropzone';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
    declarations: [
        AppComponent,
        NavBarComponent,
        FooterComponent,
        HistoricalStyleGeneratorComponent,
        AboutComponent,
        TeamMemberCardComponent,
        TeamMembersComponent,
        DemoComponent,
        SingleImageUploaderComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        BrowserAnimationsModule,
        NgbModule,
        NgxDropzoneModule,
        FormsModule,
        HttpClientModule,
        ReactiveFormsModule
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
