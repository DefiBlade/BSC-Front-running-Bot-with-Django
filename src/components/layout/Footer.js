import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import Logo from './partials/Logo';
import FooterNav from './partials/FooterNav';
import FooterSocial from './partials/FooterSocial';

const propTypes = {
  topOuterDivider: PropTypes.bool,
  topDivider: PropTypes.bool
}

const defaultProps = {
  topOuterDivider: false,
  topDivider: false
}

const Footer = ({
  className,
  topOuterDivider,
  topDivider,
  ...props
}) => {

  const classes = classNames(
    'site-footer center-content-mobile',
    topOuterDivider && 'has-top-divider',
    className
  );

  return (
    <footer
      {...props}
      className={classes}
    >
      <div className="container">
        <div className={
          classNames(
            'site-footer-inner',
            topDivider && 'has-top-divider'
          )}>
          <div className="footer-top footer-layout">
            <Logo />
            <div className="footer-bottom space-between invert-order-desktop pl-16">
              <FooterNav />
              <div className="footer-copyright text-xs">C O P Y R I G H T &nbsp; © &nbsp;   {new Date().getFullYear()}  <a href="http://localhost:8000">&nbsp; J a s o n&nbsp; </a>&nbsp; A l l &nbsp; R i g h t&nbsp;&nbsp;&nbsp;    r e s e r v e d</div>
            </div>   
          </div>

        </div>
      </div>
    </footer>
  );
}

Footer.propTypes = propTypes;
Footer.defaultProps = defaultProps;

export default Footer;