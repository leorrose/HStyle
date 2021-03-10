import { HistoricalStyleGeneratorComponent } from './historical-style-generator/historical-style-generator.component';
import { AboutComponent } from './about/about.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
    { path: '', component: AboutComponent },
    { path: 'about', component: AboutComponent },
    { path: 'get-started', component: HistoricalStyleGeneratorComponent },
    { path: '**', component: AboutComponent },
];

@NgModule({
    imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
    exports: [RouterModule]
})
export class AppRoutingModule { }
