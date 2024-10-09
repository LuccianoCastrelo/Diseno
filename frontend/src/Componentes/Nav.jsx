import React from "react";

function Nav({ Toggle }) {
  return (
    <nav className="navbar navbar-expand-sm navbar-dark bg-transparent">
      <button className="navbar-toggler" onClick={Toggle} type="button">
        <i className="bi bi-justify fs-4" />
      </button>
      <div className="collapse navbar-collapse" id="navbarContent">
        <ul className="navbar-nav ms-auto ">
          <li className="nav-item dropdown">
            <a
              className="nav-link dropdown-toggle"
              href="#"
              id="navbarDropdown"
              data-bs-toggle="dropdown"
            >
              Maquinsa
            </a>
            <ul className="dropdown-menu" aria-labelledby="navbarDropdown">
              <li>
                <a className="dropdown-item" href="#">
                  Profile
                </a>
              </li>
              <li>
                <a className="dropdown-item" href="#">
                  Settings
                </a>
              </li>
              <li>
                <a className="dropdown-item" href="#">
                  Logout
                </a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Nav;
