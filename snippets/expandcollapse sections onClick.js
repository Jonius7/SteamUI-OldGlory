                Kc = function(e) {
                    function t() {
                        var t = null !== e && e.apply(this, arguments) || this;
                        return t.state = {sExpanded: 1}, t
                    }
                    return Object(j.d)(t, e), t.prototype.expand = function() {
                        console.log("EEXPAND");
                        this.setState(function(e) {
                            return {
                                sExpanded: !e.sExpanded
                            }
                        });
                    }, t.prototype.render = function() {
                        var e = this.props,
                            t = e.className,
                            n = e.label,
                            r = e.tooltip,
                            i = e.showRule,
                            o = e.highlight,
                            a = e.feature,
                            s = e.availableOffline,
                            c = e.rightColumnSection,
                            l = e.headerClass,
                            u = Object(j.f)(e, ["className", "label", "tooltip", "showRule", "highlight", "feature", "availableOffline", "rightColumnSection", "headerClass"]);
                        return a && ko.BIsFeatureBlocked(a) || !s && E.b.OFFLINE_MODE ? null : D.createElement(wi.a, Object(j.a)({
                            className: Object(er.a)(Qc.a.AppDetailsSection, t)
                        }, u), n && D.createElement(Vc, {
                            label: n,
                            tooltip: r,
                            showRule: i,
                            className: l,
                            onClick: this.expand
                        }), this.state.sExpanded && D.createElement("div", {
                            className: Object(er.a)(Qc.a.AppDetailsSectionContainer, n && Qc.a.AppDetailsSectionHasLabel, c && Qc.a.RightColumnSection)
                        }, o, this.props.children))
                    }, t.Body = qc, t.Highlight = Zc, Object(j.c)([se.a], t.prototype, "expand", null), Object(j.c)([a.observer], t)
                }(D.Component),